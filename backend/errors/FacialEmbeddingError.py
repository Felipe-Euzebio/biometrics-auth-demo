class FacialEmbeddingError(Exception):
    """Base class for all facial embedding-related errors."""
    def __init__(self, message: str, detail: Exception = None):
        super().__init__(message)
        self.message = message
        self.detail = detail