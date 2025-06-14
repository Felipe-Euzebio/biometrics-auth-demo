from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from database import create_db_and_tables
from routers import hello, auth

# Lifespan for database initialization
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_db_and_tables()
    yield
    # Shutdown (if needed)

# FastAPI application instance
app = FastAPI(
    title="Biometrics Authentication API",
    description="A secure authentication system with biometric support",
    version="1.0.0",
    root_path="/api",  # Set the root path for the API
    lifespan=lifespan,
)

# CORS configuration to allow requests from a specific origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

# Include routers
app.include_router(hello.router)
app.include_router(auth.router)
    