from typing import Annotated
from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator
from fastapi import UploadFile
from constants import ALLOWED_IMAGE_FORMATS, MAX_IMAGE_SIZE_MB, MIN_IMAGE_RESOLUTION, MAX_IMAGE_RESOLUTION

# DTO for sign-in/sign-up
class AuthDto(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    password: str = Field(..., min_length=8, max_length=128, description="User password (minimum 8 characters)")
    
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
    @field_validator("image_data")
    def validate_image_data(cls, value: UploadFile) -> UploadFile:
        import io
        from PIL import Image, UnidentifiedImageError

        # Read the image data
        image_data = value.file.read()

        # Reset file pointer for potential future reads
        value.file.seek(0)

        # Try to open the image to validate it
        try:
            image = Image.open(io.BytesIO(image_data))

            # Check if image is empty
            if image.size == (0, 0):
                raise ValueError("Image cannot be empty")

            # Check image resolution
            width, height = image.size
            min_width, min_height = MIN_IMAGE_RESOLUTION
            max_width, max_height = MAX_IMAGE_RESOLUTION
            
            if width < min_width or height < min_height:
                raise ValueError(f"Image resolution must be at least {min_width}x{min_height} pixels")
            
            if width > max_width or height > max_height:
                raise ValueError(f"Image resolution must not exceed {max_width}x{max_height} pixels")

            # Check if image format is allowed
            if image.format.lower() not in ALLOWED_IMAGE_FORMATS:
                raise ValueError("Image must be either JPEG or PNG")
            
            # Check if image size is within limits
            if len(image_data) > MAX_IMAGE_SIZE_MB * 1024 * 1024:
                raise ValueError(f"Image size must not exceed {MAX_IMAGE_SIZE_MB} MB")
            
            return value
        except UnidentifiedImageError:
            raise ValueError("Invalid image data provided")
        
        except ValueError:
            raise

# DTO for user response
class UserDto(BaseModel):
    id: int
    email: str
    
    model_config = ConfigDict(from_attributes=True)