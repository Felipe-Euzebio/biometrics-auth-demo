from typing import Annotated
from pydantic import BaseModel, Field

# DTO for login response with JWT tokens
class LoginResponseDto(BaseModel):
    access_token: Annotated[
        str, 
        Field(..., description="JWT access token for API authentication")
    ]
    refresh_token: Annotated[
        str, 
        Field(..., description="JWT refresh token for obtaining new access tokens")
    ]
    expires_in: Annotated[
        int, 
        Field(..., description="Access token expiration time in seconds")
    ] 