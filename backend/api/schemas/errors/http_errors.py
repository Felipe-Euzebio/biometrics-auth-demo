from pydantic import BaseModel
from pydantic_core import ErrorDetails
from typing import Optional
from datetime import datetime, UTC
import traceback


class HttpError(BaseModel):
    message: str


class InternalServerError(HttpError):
    type: str
    timestamp: Optional[str] = datetime.now(UTC).isoformat()
    stacktrace: Optional[str] = traceback.format_exc()


class ValidationError(HttpError):
    details: list[ErrorDetails]