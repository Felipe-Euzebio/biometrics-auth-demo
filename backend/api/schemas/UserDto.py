from pydantic import BaseModel, ConfigDict

# DTO for user response
class UserDto(BaseModel):
    id: int
    email: str
    model_config = ConfigDict(from_attributes=True) 