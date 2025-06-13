from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator
from fastapi import UploadFile
from utils.image_utils import validate_base64_image

# DTO for sign-in/sign-up
class AuthDto(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, max_length=128, description="User password (minimum 8 characters)")
    
# DTO for user registration
class RegisterDto(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, max_length=128, description="User password (minimum 8 characters)")
    image_data: str = Field(..., description="Base64 encoded image data for biometric profile")

    # Validator to ensure image is either JPEG or PNG and properly formatted
    @field_validator("image_data")
    def validate_image_data(cls, value: str) -> str:
        is_valid, exception = validate_base64_image(value)
        
        if not is_valid and exception:
            raise exception
        
        return value

# DTO for user response
class UserDto(BaseModel):
    id: int
    email: str
    
    model_config = ConfigDict(from_attributes=True)