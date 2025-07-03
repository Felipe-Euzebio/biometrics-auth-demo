import io
from typing import Optional
from fastapi import UploadFile
from PIL import Image, UnidentifiedImageError
from api.constants import ALLOWED_IMAGE_FORMATS, MAX_IMAGE_SIZE_MB, MIN_IMAGE_RESOLUTION, MAX_IMAGE_RESOLUTION

def validate_password(
    password: str,
    min_length: int = 8,
    max_length: int = 32,
    require_digit: bool = True,
    require_lowercase: bool = True,
    require_uppercase: bool = True,
    require_non_alphanumeric: bool = True
) -> str:
    """
    Validate password strength according to specified requirements.
    
    Args:
        password: The password to validate
        min_length: Minimum password length (default: 8)
        max_length: Maximum password length (default: 32)
        require_digit: Whether to require at least one digit (default: True)
        require_lowercase: Whether to require at least one lowercase letter (default: True)
        require_uppercase: Whether to require at least one uppercase letter (default: True)
        require_non_alphanumeric: Whether to require at least one non-alphanumeric character (default: True)
    
    Returns:
        The validated password string
    
    Raises:
        ValueError: If password doesn't meet the requirements
    """
    errors = []
    
    # Check length requirements
    if len(password) < min_length:
        errors.append(f"at least {min_length} characters")
    if len(password) > max_length:
        errors.append(f"no more than {max_length} characters")
    
    # Check character requirements
    if require_digit and not any(c.isdigit() for c in password):
        errors.append("at least one digit")
    if require_lowercase and not any(c.islower() for c in password):
        errors.append("at least one lowercase letter")
    if require_uppercase and not any(c.isupper() for c in password):
        errors.append("at least one uppercase letter")
    if require_non_alphanumeric and all(c.isalnum() for c in password):
        errors.append("at least one non-alphanumeric character")
        
    if errors:
        reqs = ", ".join(errors)
        raise ValueError(f"Password must contain {reqs}")
    
    return password

def validate_image_data(image_data: Optional[UploadFile]) -> Optional[UploadFile]:
    """
    Validate uploaded image data according to application requirements.
    
    This function performs comprehensive validation of image files including:
    - Format validation (JPEG, PNG or WebP only)
    - Resolution constraints (minimum and maximum dimensions)
    - File size limits
    - Image integrity checks
    
    Args:
        image_data: The uploaded image file to validate, or None if no image provided
    
    Returns:
        The validated UploadFile object if validation passes, or None if no image provided
    
    Raises:
        ValueError: If image doesn't meet any of the validation requirements:
            - Empty image (0x0 pixels)
            - Resolution below minimum requirements
            - Resolution above maximum requirements
            - Unsupported image format
            - File size exceeds maximum allowed size
            - Invalid or corrupted image data
    
    Note:
        The function resets the file pointer after reading, so the image data
        can be read again by subsequent operations.
    """
    if image_data is None:
        return None
    
    # Read the image data
    image_bytes = image_data.file.read()
    
    # Reset file pointer for potential future reads
    image_data.file.seek(0)
    
    # Try to open the image to validate it
    try:
        image = Image.open(io.BytesIO(image_bytes))
        
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
            raise ValueError("Image must be either JPEG, PNG or WebP")
        
        # Check if image size is within limits
        if len(image_bytes) > MAX_IMAGE_SIZE_MB * 1024 * 1024:
            raise ValueError(f"Image size must not exceed {MAX_IMAGE_SIZE_MB} MB")
        
        return image_data
    
    except UnidentifiedImageError:
        raise ValueError("Invalid image data provided")
