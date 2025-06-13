import io
import base64
from PIL import Image
from typing import Optional
from backend.constants import ALLOWED_IMAGE_FORMATS

def validate_base64_image(image_data: str) -> tuple[bool, Optional[Exception]]:
    """
    Validates base64 encoded image data.
    
    Args:
        image_data (str): Base64 encoded image string
        
    Returns:
        tuple[bool, Optional[Exception]]: (is_valid, exception_object)
    """
    try:
        # Decode base64 data
        decoded_data = base64.b64decode(image_data, validate=True)
        
        # Open image to validate format
        image = Image.open(io.BytesIO(decoded_data))
        
        # Check if image format is allowed
        if image.format.lower() not in ALLOWED_IMAGE_FORMATS:
            return False, ValueError("Image must be either JPEG or PNG")
        
        return True, None
        
    except (ValueError, TypeError) as e:
        return False, ValueError("Image data must be a valid base64 encoded string")
    except IOError as e:
        return False, ValueError("Invalid image data")
    except Exception as e:
        return False, e 