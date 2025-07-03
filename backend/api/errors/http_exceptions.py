from fastapi import HTTPException


class BadRequestError(HTTPException):
    """HTTP 400 Bad Request error."""
    def __init__(self, detail: str = "Bad Request"):
        super().__init__(status_code=400, detail=detail)


class UnauthorizedError(HTTPException):
    """HTTP 401 Unauthorized error."""
    def __init__(self, detail: str = "Unauthorized"):
        super().__init__(status_code=401, detail=detail)


class ForbiddenError(HTTPException):
    """HTTP 403 Forbidden error."""
    def __init__(self, detail: str = "Forbidden"):
        super().__init__(status_code=403, detail=detail)


class NotFoundError(HTTPException):
    """HTTP 404 Not Found error."""
    def __init__(self, detail: str = "Not Found"):
        super().__init__(status_code=404, detail=detail)


class InternalServerError(HTTPException):
    """HTTP 500 Internal Server Error."""
    def __init__(self, detail: str = "Internal Server Error"):
        super().__init__(status_code=500, detail=detail) 