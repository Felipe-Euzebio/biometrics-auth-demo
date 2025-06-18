from typing import Annotated, Optional
from pydantic import BaseModel, Field

# DTO for login response with JWT tokens
class AuthenticatedDto(BaseModel):
    access_token: Annotated[
        str, 
        Field(..., description="JWT access token for API authentication")
    ]
    refresh_token: Annotated[
        Optional[str], 
        Field(None, description="JWT refresh token for obtaining new access tokens")
    ]