from pydantic import BaseModel, Field
from typing import Annotated

class NewAccessTokenDto(BaseModel):
    access_token: Annotated[
        str, 
        Field(..., description="New JWT access token for API authentication")
    ]