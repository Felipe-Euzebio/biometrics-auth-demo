from fastapi import Request
from sqlmodel import Session, select
from api.models import User, BiometricProfile
from api.schemas import LoginDto, RegisterDto, AuthenticatedDto, RefreshTokenDto, NewAccessTokenDto, UserDto
from api.utils.deepface_utils import generate_facial_embedding, verify_facial_embeddings
from api.errors import BadRequestError, UnauthorizedError, NotFoundError, InternalServerError
from argon2 import PasswordHasher
from authx import AuthX, TokenPayload, RequestToken
from authx.types import TokenLocation
from authx.exceptions import InvalidToken, JWTDecodeError, TokenTypeError, AccessTokenRequiredError, FreshTokenRequiredError

# Create password hasher instance here to avoid circular import
_ph = PasswordHasher(
    time_cost=3,          # Number of iterations
    memory_cost=65536,    # Memory usage (64MB)
    parallelism=2,        # Number of parallel threads
    hash_len=32,          # Hash length (32 bytes = 256 bits)
    salt_len=16           # Salt length (16 bytes = 128 bits)
)

class AuthService:
    def __init__(self, session: Session, authx: AuthX):
        self.session = session
        self.authx = authx

    async def _get_user_by_email(self, email: str) -> User | None:
        statement = select(User).where(User.email == email)
        return self.session.exec(statement).first()
    
    def _generate_auth_tokens(self, user_id: str) -> tuple[str, str]:
        """
        Generate access and refresh tokens for a user.
        
        Args:
            user_id: The user ID to generate tokens for
            
        Returns:
            tuple[str, str]: (access_token, refresh_token)
            
        Raises:
            InternalServerError: If token generation fails
        """
        try:
            access_token = self.authx.create_access_token(
                uid=user_id,
                expiry=self.authx.config.JWT_ACCESS_TOKEN_EXPIRES
            )
            refresh_token = self.authx.create_refresh_token(
                uid=user_id,
                expiry=self.authx.config.JWT_REFRESH_TOKEN_EXPIRES
            )
            return access_token, refresh_token
        except Exception as e:
            raise InternalServerError(f"Failed to generate authentication tokens: {str(e)}")
    
    def _verify_token(self, token: str, location: TokenLocation, token_type: str = "access") -> TokenPayload:
        """
        Verify a JWT token and return the payload.
        
        Args:
            token: The JWT token to verify
            location: Where the token was found (headers, json, etc.)
            token_type: The expected token type (access, refresh)
            
        Returns:
            TokenPayload: The decoded token payload
            
        Raises:
            UnauthorizedError: If token verification fails
        """
        try:
            return self.authx.verify_token(
                token=RequestToken(token=token, location=location, type=token_type),
                verify_type=True
            )
        except (InvalidToken, JWTDecodeError, TokenTypeError, AccessTokenRequiredError, FreshTokenRequiredError) as e:
            raise UnauthorizedError(f"Token verification failed: {str(e)}")
        except Exception as e:
            raise InternalServerError(f"Unexpected error during token verification: {str(e)}")
    
    async def register(self, request: RegisterDto) -> AuthenticatedDto:
        try:
            # If the user already exists, raise an error
            if await self._get_user_by_email(request.email):
                raise BadRequestError("User already exists")
            
            # Generate facial embedding first to validate the image data
            facial_embedding = generate_facial_embedding(request.image_data)

            # Create user with hashed password
            user = User(
                email=request.email,
                password=_ph.hash(request.password)
            )

            # Add the user to the database (but don't commit yet)
            self.session.add(user)
            self.session.flush()  # Flush to get the user ID without committing

            # Create a new BiometricProfile for the user
            biometric_profile = BiometricProfile(
                user_id=user.id,
                facial_embedding=facial_embedding
            )

            # Add the biometric profile to the database
            self.session.add(biometric_profile)
            
            # Commit both user and biometric profile together
            self.session.commit()
            self.session.refresh(user)

            # Generate authentication tokens
            access_token, refresh_token = self._generate_auth_tokens(str(user.id))

            # Return the access and refresh tokens for the authenticated user
            return AuthenticatedDto(
                access_token=access_token,
                refresh_token=refresh_token
            )
        
        except BadRequestError as e:
            raise e
        
        except (UnauthorizedError, InternalServerError) as e:
            raise e
        
        except ValueError as e:
            raise BadRequestError(str(e))
        
        except Exception as e:
            raise InternalServerError(str(e))
    
    async def login(self, request: LoginDto) -> AuthenticatedDto:
        try:
            user = await self._get_user_by_email(request.email)

            # If the user with the provided email doesn't exist, raise an error
            if not user:
                raise UnauthorizedError("Invalid email or password")
            
            # If password is provided, verify it
            if request.password and not _ph.verify(user.password, request.password):
                raise UnauthorizedError("Invalid email or password")
            
            # If image_data is provided, generate facial embedding
            if request.image_data:
                # If the user doesn't have a biometric profile, raise an error
                if not user.biometric_profile:
                    raise BadRequestError("No biometric profile found for this user")
                
                # Generate embedding from uploaded image
                facial_embedding = generate_facial_embedding(request.image_data)

                # Verify the facial embedding against the stored profile
                if not verify_facial_embeddings(facial_embedding, user.biometric_profile.facial_embedding):
                    raise UnauthorizedError("Facial authentication failed")
            
            # Generate authentication tokens
            access_token, refresh_token = self._generate_auth_tokens(str(user.id))

            # Return the access and refresh tokens for the authenticated user
            return AuthenticatedDto(
                access_token=access_token,
                refresh_token=refresh_token
            )
        
        except (BadRequestError, UnauthorizedError, InternalServerError) as e:
            raise e
        
        except ValueError as e:
            raise BadRequestError(str(e))
        
        except Exception as e:
            raise InternalServerError(str(e))
    
    async def refresh(
        self, 
        request: Request, 
        refresh_data: RefreshTokenDto = None
    ) -> NewAccessTokenDto:
        try:
            # Get the token from the Authorization header
            auth_header = request.headers.get("Authorization")
            token: str = None
            token_location: TokenLocation = None

            # If the Authorization header is present, extract the token.
            # If the Authorization header is not present, check if the token is provided in the request body.
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.split(" ")[1]
                token_location = "headers"
            elif refresh_data and refresh_data.refresh_token:
                token = refresh_data.refresh_token
                token_location = "json"

            # If no token is found, raise an error
            if not token:
                raise BadRequestError("Refresh token is required")
            
            # Verify the refresh token
            refresh_payload = self._verify_token(token, token_location, "refresh")

            # Create new access token
            access_token = self.authx.create_access_token(
                uid=str(refresh_payload.sub),
                expiry=self.authx.config.JWT_ACCESS_TOKEN_EXPIRES
            )

            # Return the new access token
            return NewAccessTokenDto(access_token=access_token)
        
        except (BadRequestError, UnauthorizedError, InternalServerError) as e:
            raise e
        
        except Exception as e:
            raise InternalServerError(str(e))
        
    async def get_current_user(self, request: Request) -> UserDto:
        try:
            # Get the token from the Authorization header
            auth_header = request.headers.get("Authorization")
            token = auth_header.split(" ")[1]

            # Verify the access token
            token_payload = self._verify_token(token, "headers", "access")

            # Fetch the user by ID from the database
            user = self.session.get(User, token_payload.sub)

            # If the user is not found, raise an error
            if not user:
                raise NotFoundError("User not found")

            return UserDto.model_validate(user)
        
        except (NotFoundError, UnauthorizedError, InternalServerError) as e:
            raise e
        
        except Exception as e:
            raise InternalServerError(str(e))

    