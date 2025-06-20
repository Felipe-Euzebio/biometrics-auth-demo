from typing import Annotated
from pydantic import BaseModel, Field

class RefreshTokenDto(BaseModel):
    refresh_token: Annotated[
        str, 
        Field(..., description="JWT refresh token to obtain new access tokens")
    ]