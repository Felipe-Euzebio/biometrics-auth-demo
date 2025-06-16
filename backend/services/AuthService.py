from fastapi import HTTPException
from sqlmodel import Session, select
from models import User, BiometricProfile
from schemas import LoginDto, UserDto, RegisterDto
from utils.deepface_utils import generate_facial_embedding, verify_facial_embeddings
from errors.facial_embedding_error import FacialEmbeddingError
from argon2 import PasswordHasher

# Create password hasher instance here to avoid circular import
password_hasher = PasswordHasher(
    time_cost=3,          # Number of iterations
    memory_cost=65536,    # Memory usage (64MB)
    parallelism=2,        # Number of parallel threads
    hash_len=32,          # Hash length (32 bytes = 256 bits)
    salt_len=16           # Salt length (16 bytes = 128 bits)
)

class AuthService:
    def __init__(self, session: Session):
        self.session = session
    
    async def register(self, request: RegisterDto) -> UserDto:
        # Check if user already exists
        statement = select(User).where(User.email == request.email)
        existing_user = self.session.exec(statement).first()

        # If the user already exists, raise an error
        if existing_user:
            raise HTTPException(status_code=400, detail="User already exists")
        
        # Generate facial embedding first to validate the image data
        try:
            facial_embedding = generate_facial_embedding(request.image_data)
        except FacialEmbeddingError as e:
            raise HTTPException(status_code=400, detail=str(e))

        # Create user with hashed password
        user = User(
            email=request.email,
            password=password_hasher.hash(request.password)
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

        # Map user to UserDto
        return UserDto.model_validate(user)
    
    async def login(self, request: LoginDto) -> UserDto:
        # Find user by email
        statement = select(User).where(User.email == request.email)
        db_user = self.session.exec(statement).first()

        # User doesn't exist
        if not db_user:
            raise HTTPException(status_code=400, detail="Invalid email or password")
        
        # Password authentication
        if request.password and not password_hasher.verify(db_user.password, request.password):
            raise HTTPException(status_code=400, detail="Invalid email or password")
        
        # Facial authentication
        if request.image_data:
            # User must have a biometric profile for facial auth
            if not db_user.biometric_profile:
                raise HTTPException(status_code=400, detail="No biometric profile found for this user")
            
            try:
                # Generate embedding from uploaded image and verify against stored profile
                facial_embedding = generate_facial_embedding(request.image_data)

                if not verify_facial_embeddings(facial_embedding, db_user.biometric_profile.facial_embedding):
                    raise HTTPException(status_code=400, detail="Facial authentication failed")
                
            except FacialEmbeddingError as e:
                raise HTTPException(status_code=400, detail=str(e))
        
        # Authentication successful - return user data
        return UserDto.model_validate(db_user)
    