from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from contextlib import asynccontextmanager
from api.database import create_db_and_tables
from api.routers import hello, auth
from api.dependencies import authx
from api.config import settings
from fastapi import HTTPException
from fastapi.exceptions import RequestValidationError
from api.errors.exception_handlers import (
    http_exception_handler, 
    validation_exception_handler, 
    server_error_handler
)

# Lifespan for database initialization
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_db_and_tables()
    yield
    # Shutdown (if needed)

# FastAPI application instance
app = FastAPI(
    title="Facial Authentication API",
    description="A secure facial authentication system",
    version="1.0.0",
    root_path="/api",  # Set the root path for the API
    lifespan=lifespan
)

# Register custom exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, server_error_handler)

# Configure AuthX error handling
authx.handle_errors(app)

# CORS configuration to allow requests from configured origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Custom OpenAPI configuration to enable Authorization header persistence
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    
    # Add security schemes
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter your JWT access token (without Bearer prefix)"
        }
    }
    
    # Add global security requirement
    openapi_schema["security"] = [
        {
            "BearerAuth": []
        }
    ]
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Include routers
app.include_router(hello.router)
app.include_router(auth.router)
    