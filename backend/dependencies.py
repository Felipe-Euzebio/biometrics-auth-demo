from typing import Annotated
from fastapi import Depends
from sqlmodel import Session
from database import get_session
from services import AuthService
from authx import AuthX, AuthXConfig
from config import settings

# Database session dependency that can be used across all routers
SessionDep = Annotated[Session, Depends(get_session)]

# AuthX Configuration - Global singleton
authx_config = AuthXConfig(
    JWT_ALGORITHM=settings.jwt_algorithm,
    JWT_SECRET_KEY=settings.jwt_secret_key,
    JWT_TOKEN_LOCATION=["headers"],
    JWT_ACCESS_TOKEN_EXPIRES=settings.jwt_access_token_expires,
    JWT_REFRESH_TOKEN_EXPIRES=settings.jwt_refresh_token_expires,
)

# Global AuthX instance
authx = AuthX(config=authx_config)

def create_auth_service(session: SessionDep) -> AuthService:
    return AuthService(session)

AuthServiceDep = Annotated[AuthService, Depends(create_auth_service)]

AuthXDep = Annotated[AuthX, Depends(lambda: authx)] 