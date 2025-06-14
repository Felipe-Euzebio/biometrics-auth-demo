from typing import Annotated
from fastapi import Depends
from sqlmodel import Session
from database import get_session
from argon2 import PasswordHasher

# Database session dependency that can be used across all routers
SessionDep = Annotated[Session, Depends(get_session)]

# Password hasher dependency for hashing and verifying passwords
password_hasher = PasswordHasher(
    time_cost=3,          # Number of iterations
    memory_cost=65536,    # Memory usage (64MB)
    parallelism=2,        # Number of parallel threads
    hash_len=32,          # Hash length (32 bytes = 256 bits)
    salt_len=16           # Salt length (16 bytes = 128 bits)
) 