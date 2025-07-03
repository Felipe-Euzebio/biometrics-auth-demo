from typing import Optional, Annotated
from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator
from fastapi import UploadFile
from api.validators.field_validators import validate_image_data

# DTO for login with either password or facial recognition
class LoginDto(BaseModel):
    email: Annotated[
        EmailStr, 
        Field(..., description="User email address")
    ]
    password: Annotated[
        Optional[str],
        Field(None, description="User password")
    ]
    image_data: Annotated[
        Optional[UploadFile], 
        Field(None, description="Uploaded image file for facial recognition")
    ]

    @model_validator(mode='after')
    def validate_auth_method(self) -> 'LoginDto':
        """Ensure either password or image_data is provided, but not both"""
        if self.password is None and self.image_data is None:
            raise ValueError("Either password or image_data must be provided for authentication")
        
        if self.password is not None and self.image_data is not None:
            raise ValueError("Cannot provide both password and image_data. Choose one authentication method")
        
        return self

    # Validator to ensure image data is valid
    _validate_image_data = field_validator("image_data")(validate_image_data)