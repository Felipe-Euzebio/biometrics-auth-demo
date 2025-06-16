from typing import Annotated
from fastapi import Depends
from sqlmodel import Session
from database import get_session
from services import AuthService

# Database session dependency that can be used across all routers
SessionDep = Annotated[Session, Depends(get_session)]

def create_auth_service(session: Session) -> AuthService:
    return AuthService(session)

AuthServiceDep = Annotated[AuthService, Depends(create_auth_service)] 