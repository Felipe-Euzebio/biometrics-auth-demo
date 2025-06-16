from fastapi import APIRouter, HTTPException, Form
from dependencies import SessionDep, password_hasher
from models import User, BiometricProfile
from sqlmodel import select
from schemas import LoginDto, UserDto, RegisterDto
from utils.deepface_utils import generate_facial_embedding, verify_facial_embeddings
from errors.facial_embedding_error import FacialEmbeddingError

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
async def register(
    session: SessionDep,
    request: RegisterDto = Form(..., media_type="multipart/form-data")
):
    # Check if user already exists
    statement = select(User).where(User.email == request.email)
    existing_user = session.exec(statement).first()

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
    session.add(user)
    session.flush()  # Flush to get the user ID without committing

    # Create a new BiometricProfile for the user
    biometric_profile = BiometricProfile(
        user_id=user.id,
        facial_embedding=facial_embedding
    )

    # Add the biometric profile to the database
    session.add(biometric_profile)
    
    # Commit both user and biometric profile together
    session.commit()
    session.refresh(user)

    # Map user to UserDto
    return UserDto.model_validate(user)

@router.post("/login")
async def login(
    session: SessionDep,
    request: LoginDto = Form(..., media_type="multipart/form-data"), 
):
    # Find user by email
    statement = select(User).where(User.email == request.email)
    db_user = session.exec(statement).first()

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
