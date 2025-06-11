from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict

# DTO for sign-in/sign-up
class AuthDto(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, max_length=128, description="User password (minimum 8 characters)")

# DTO for user response
class UserDto(BaseModel):
    id: int
    email: str
    
    model_config = ConfigDict(from_attributes=True)