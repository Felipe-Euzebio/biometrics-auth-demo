from fastapi import APIRouter, HTTPException
from dependencies import SessionDep
from models.user import User
from argon2 import PasswordHasher
from sqlmodel import select
from schemas.user import AuthDto, UserDto

router = APIRouter(prefix="/auth", tags=["auth"])

# Initialize hasher with secure parameters
ph: PasswordHasher = PasswordHasher(
    time_cost=3,          # Number of iterations
    memory_cost=65536,    # Memory usage (64MB)
    parallelism=2,        # Number of parallel threads
    hash_len=32,          # Hash length (32 bytes = 256 bits)
    salt_len=16           # Salt length (16 bytes = 128 bits)
)

@router.post("/register")
async def register(dto: AuthDto, session: SessionDep):
    # Check if user already exists
    statement = select(User).where(User.email == dto.email)
    existing_user = session.exec(statement).first()

    # If the user already exists, raise an error
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")
    
    # Create user with hashed password
    user = User(
        email=dto.email,
        password=ph.hash(dto.password)
    )

    # Add the user to the database
    session.add(user)
    session.commit()
    session.refresh(user)

    # Map user to UserDto
    return UserDto.model_validate(user)

@router.post("/login")
async def login(dto: AuthDto, session: SessionDep):
    # Check if user exists
    statement = select(User).where(User.email == dto.email)
    db_user = session.exec(statement).first()

    # If user does not exist or password is incorrect, raise an error
    if not db_user or not ph.verify(db_user.password, dto.password):
        raise HTTPException(status_code=400, detail="Invalid email or password")
    
    # Map db_user to UserDto
    return UserDto.model_validate(db_user)
