from typing import Annotated
from fastapi import Depends
from sqlmodel import Session
from database import get_session

# Database session dependency that can be used across all routers
SessionDep = Annotated[Session, Depends(get_session)] 