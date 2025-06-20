from sqlmodel import SQLModel, create_engine, Session
from api import models # Side-effect import to ensure models are registered

# Database URL - using SQLite for simplicity
DATABASE_URL = "sqlite:///biometrics_auth.db"

# Create engine
engine = create_engine(
    DATABASE_URL, 
    echo=True,  # Set to False in production
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

def create_db_and_tables():
    """Create database tables based on SQLModel definitions."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Get a database session."""
    with Session(engine) as session:
        yield session 