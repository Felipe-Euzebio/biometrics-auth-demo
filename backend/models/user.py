from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from models import BiometricProfile  # Avoid circular import issues

class User(SQLModel, table=True):
    """User model for authentication and user management."""
    
    id: int | None = Field(default=None, primary_key=True, index=True)
    email: str = Field(unique=True, index=True, max_length=255)
    password: str = Field(max_length=255) 

    biometric_profile: Optional["BiometricProfile"] = Relationship(
        back_populates="user",
        sa_relationship_kwargs={"uselist": False}
    )