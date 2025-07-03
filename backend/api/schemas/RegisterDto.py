from typing import Annotated
from pydantic import BaseModel, Field, EmailStr, field_validator
from fastapi import UploadFile
from api.validators.field_validators import validate_password, validate_image_data

# DTO for user registration
class RegisterDto(BaseModel):
    email: Annotated[EmailStr, Field(..., description="User email address")]
    password: Annotated[
        str, 
        Field(..., min_length=8, max_length=32, description="User password (8 - 32 characters)")
    ]
    image_data: Annotated[
        UploadFile,
        Field(..., description="Uploaded image file for facial recognition")
    ]

    # Validator to ensure password meets requirements
    _validate_password = field_validator("password")(validate_password)
    
    # Validator to ensure image data is valid
    _validate_image_data = field_validator("image_data")(validate_image_data)