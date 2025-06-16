from typing import TYPE_CHECKING, Optional
from sqlmodel import SQLModel, Field, Relationship, Column, BLOB, DateTime, func
from datetime import datetime, UTC
import numpy as np

if TYPE_CHECKING:
    from models import User  # Avoid circular import issues

class BiometricProfile(SQLModel, table=True):
    """Biometric profile model for storing user biometric data."""	

    id: int | None = Field(default=None, primary_key=True, index=True)
    user_id: int | None = Field(default=None, foreign_key="user.id", index=True)
    facial_embedding: bytes = Field(sa_column=Column(BLOB))

    # Audit timestamps
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column=Column(DateTime(timezone=True), server_default=func.now())
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        sa_column=Column(DateTime(timezone=True), onupdate=func.now())
    )

    user: Optional["User"] = Relationship(back_populates="biometric_profile")

    # Property to handle conversion between bytes and list of floats
    @property
    def embedding_array(self) -> list[float]:
        return np.frombuffer(self.facial_embedding, dtype=np.float32).tolist()
    
    # Setter to convert list of floats to bytes
    @embedding_array.setter
    def embedding_array(self, value: list[float]):
        self.facial_embedding = np.array(value, dtype=np.float32).tobytes()