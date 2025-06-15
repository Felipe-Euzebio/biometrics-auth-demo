from typing import Annotated
from pydantic import BaseModel, Field, EmailStr, field_validator
from fastapi import UploadFile
from validators.image_validators import validate_image_data

# DTO for user registration
class RegisterDto(BaseModel):
    email: Annotated[EmailStr, Field(..., description="User email address")]
    password: Annotated[
        str, 
        Field(..., min_length=8, max_length=128, description="User password (minimum 8 characters)")
    ]
    image_data: Annotated[
        UploadFile,
        Field(..., description="Uploaded image file for facial recognition")
    ]

    # Validator to ensure image data is valid
    validate_image_data = field_validator("image_data")(validate_image_data)