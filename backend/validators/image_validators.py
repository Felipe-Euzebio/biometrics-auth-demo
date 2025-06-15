import io
from typing import Optional
from fastapi import UploadFile
from PIL import Image, UnidentifiedImageError
from constants import ALLOWED_IMAGE_FORMATS, MAX_IMAGE_SIZE_MB, MIN_IMAGE_RESOLUTION, MAX_IMAGE_RESOLUTION

def validate_image_data(image_data: Optional[UploadFile]) -> Optional[UploadFile]:
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
            raise ValueError("Image must be either JPEG or PNG")
        
        # Check if image size is within limits
        if len(image_bytes) > MAX_IMAGE_SIZE_MB * 1024 * 1024:
            raise ValueError(f"Image size must not exceed {MAX_IMAGE_SIZE_MB} MB")
        
        return image_data
    
    except UnidentifiedImageError:
        raise ValueError("Invalid image data provided") from None
