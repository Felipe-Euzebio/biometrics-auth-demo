from sqlmodel import SQLModel, Field, Relationship
from models.biometric_profile import BiometricProfile

class User(SQLModel, table=True):
    """User model for authentication and user management."""
    
    id: int | None = Field(default=None, primary_key=True, index=True)
    email: str = Field(unique=True, index=True, max_length=255)
    password: str = Field(max_length=255) 

    biometric_profile: BiometricProfile | None = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"uselist": False}
    )