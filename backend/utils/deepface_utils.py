import io
import numpy as np
from deepface import DeepFace
from PIL import Image
from fastapi import UploadFile
from errors.facial_embedding_error import FacialEmbeddingError
from constants import DEFAULT_MODEL_NAME

def generate_facial_embedding(image_file: UploadFile) -> bytes:
    """
    Generate facial embedding from an uploaded image file.

    Args:
        image_file: UploadFile containing the image data

    Returns:
        bytes: Facial embedding as a byte array
    
    Raises:
        FacialEmbeddingError: If the image cannot be processed or embedding generation fails
    """
    try:
        # Read image data
        image_data = image_file.file.read()
        image_file.file.seek(0)  # Reset file pointer for potential future reads

        # Convert to PIL Image
        image = Image.open(io.BytesIO(image_data))

        # Convert to RGB if necessary (DeepFace expects RGB)
        if image.mode != 'RGB':
            image = image.convert('RGB')

        # Convert PIL Image to numpy array
        image_array = np.array(image)

        # Generate embedding using DeepFace
        embedding_result = DeepFace.represent(
            img_path=image_array,
            model_name=DEFAULT_MODEL_NAME,  # Using Facenet512 for high-quality embeddings
            detector_backend="opencv",
            enforce_detection=True,
            align=True
        )
        
        # DeepFace.represent returns a list of dictionaries, extract the embedding vector
        if not embedding_result:
            raise FacialEmbeddingError(
                message="No face detected in the provided image.",
                detail=None
            )
        
        # Check if multiple faces are detected (only one face is allowed for biometric authentication)
        if len(embedding_result) > 1:
            raise FacialEmbeddingError(
                message=f"Multiple faces detected in the image. Only one face is allowed for biometric authentication. Found {len(embedding_result)} faces.",
                detail=None
            )
        
        # Get the first face's embedding (assuming single face)
        embedding_vector = embedding_result[0]["embedding"]
        
        # Convert embedding to numpy array and then to bytes
        embedding_array = np.array(embedding_vector, dtype=np.float32)
        embedding_bytes = embedding_array.tobytes()

        return embedding_bytes
    
    except FacialEmbeddingError as e:
        raise FacialEmbeddingError(
            message="Failed to generate facial embedding from the provided image.",
            detail=e
        )
    
def verify_facial_embeddings(
    embedding1_bytes: bytes,
    embedding2_bytes: bytes,
) -> bool:
    """
    Compare two facial embeddings and return similarity score using DeepFace's verify method.

    Args:
        embedding1_bytes: First facial embedding as bytes
        embedding2_bytes: Second facial embedding as bytes

    Returns:
        bool: True if embeddings match, False otherwise
    """
    # Convert bytes back to numpy arrays
    embedding1_array = np.frombuffer(embedding1_bytes, dtype=np.float32)
    embedding2_array = np.frombuffer(embedding2_bytes, dtype=np.float32)

    # Use DeepFace's verify method with pre-calculated embeddings
    result = DeepFace.verify(
        img1_path=embedding1_array,
        img2_path=embedding2_array,
        model_name=DEFAULT_MODEL_NAME,
        detector_backend="opencv",
        enforce_detection=False,  # Since we already have embeddings
        align=False,  # Since we already have embeddings
        distance_metric="cosine",
    )
    
    return result["verified"]