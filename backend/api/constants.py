# Application-wide constants

# Allowed image formats for user biometric profile
ALLOWED_IMAGE_FORMATS = ["png", "jpeg", "webp"] 

# Maximum allowed image size in MB for user biometric profile
MAX_IMAGE_SIZE_MB = 5

# Minimum image resolution for facial recognition (width x height)
MIN_IMAGE_RESOLUTION = (100, 100)

# Maximum image resolution for facial recognition (width x height)
MAX_IMAGE_RESOLUTION = (4096, 4096)

# Default model name for facial embeddings
DEFAULT_MODEL_NAME = "Facenet512"