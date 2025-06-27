from fastapi import Request
from sqlmodel import Session, select
from api.models import User, BiometricProfile
from api.schemas import LoginDto, RegisterDto, AuthenticatedDto, RefreshTokenDto, NewAccessTokenDto, UserDto
from api.utils.deepface_utils import generate_facial_embedding, verify_facial_embeddings
from api.errors import BadRequestError, UnauthorizedError, NotFoundError, InternalServerError
from argon2 import PasswordHasher
from authx import AuthX, TokenPayload, RequestToken
from authx.types import TokenLocation

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

            # Create access and refresh tokens using AuthX
            access_token = self.authx.create_access_token(
                uid=str(user.id),
                expiry=self.authx.config.JWT_ACCESS_TOKEN_EXPIRES
            )
            refresh_token = self.authx.create_refresh_token(
                uid=str(user.id),
                expiry=self.authx.config.JWT_REFRESH_TOKEN_EXPIRES
            )

            # Return the access and refresh tokens for the authenticated user
            return AuthenticatedDto(
                access_token=access_token,
                refresh_token=refresh_token
            )
        
        except (BadRequestError, UnauthorizedError, NotFoundError) as e:
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
                raise BadRequestError("Invalid email or password")
            
            # If password is provided, verify it
            if request.password and not _ph.verify(user.password, request.password):
                raise BadRequestError("Invalid email or password")
            
            # If image_data is provided, generate facial embedding
            if request.image_data:
                # If the user doesn't have a biometric profile, raise an error
                if not user.biometric_profile:
                    raise BadRequestError("No biometric profile found for this user")
                
                # Generate embedding from uploaded image
                facial_embedding = generate_facial_embedding(request.image_data)

                # Verify the facial embedding against the stored profile
                if not verify_facial_embeddings(facial_embedding, user.biometric_profile.facial_embedding):
                    raise BadRequestError("Facial authentication failed")
            
            # Create access and refresh tokens using AuthX
            access_token = self.authx.create_access_token(
                uid=str(user.id),
                expiry=self.authx.config.JWT_ACCESS_TOKEN_EXPIRES
            )
            refresh_token = self.authx.create_refresh_token(
                uid=str(user.id),
                expiry=self.authx.config.JWT_REFRESH_TOKEN_EXPIRES
            )

            # Return the access and refresh tokens for the authenticated user
            return AuthenticatedDto(
                access_token=access_token,
                refresh_token=refresh_token
            )
        
        except (BadRequestError, UnauthorizedError, NotFoundError) as e:
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
            refresh_payload: TokenPayload = self.authx.verify_token(
                token=RequestToken(token=token, location=token_location, type="refresh"),
                verify_type=True
            )

            # Create new access token
            access_token = self.authx.create_access_token(
                uid=str(refresh_payload.sub),
                expiry=self.authx.config.JWT_ACCESS_TOKEN_EXPIRES
            )

            # Return the new access token
            return NewAccessTokenDto(access_token=access_token)
        
        except (BadRequestError, UnauthorizedError, NotFoundError) as e:
            raise e
        
        except Exception as e:
            raise InternalServerError(str(e))
        
    async def get_current_user(self, request: Request) -> UserDto:
        try:
            # Get the token from the Authorization header
            auth_header = request.headers.get("Authorization")
            token = auth_header.split(" ")[1]

            # Verify the access token
            token_payload: TokenPayload = self.authx.verify_token(
                token=RequestToken(token=token, location="headers"),
                verify_type=True
            )

            # Fetch the user by ID from the database
            user = self.session.get(User, token_payload.sub)

            # If the user is not found, raise an error
            if not user:
                raise NotFoundError("User not found")

            return UserDto.model_validate(user)
        
        except (BadRequestError, UnauthorizedError, NotFoundError) as e:
            raise e
        
        except Exception as e:
            raise InternalServerError(str(e))

    