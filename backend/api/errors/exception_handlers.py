from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from api.schemas import InternalServerError, ValidationError, HttpError


# Handler for server errors (500)
async def server_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=InternalServerError(
            message="Oops! An unexpected error ocurred. Please, try again later.",
            type=type(exc).__name__
        ).model_dump()
    )


# Handler for validation errors (422)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=ValidationError(
            message="Please check your input and try again. Some fields may be missing or contain invalid data.",
            details=exc.errors()
        ).model_dump()
    )


# Handler for other HTTP errors
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=HttpError(
            message=exc.detail if isinstance(exc.detail, str) else str(exc.detail)
        ).model_dump()
    ) 