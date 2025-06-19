from typing import Annotated
from pydantic import BaseModel, Field

# DTO for login response with JWT tokens
class AuthenticatedDto(BaseModel):
    access_token: Annotated[
        str, 
        Field(..., description="JWT access token for API authentication")
    ]
    refresh_token: Annotated[
        str, 
        Field(None, description="JWT refresh token for obtaining new access tokens")
    ]