from fastapi import APIRouter

router = APIRouter(prefix="/hello", tags=["hello"])

# Define a simple route for testing
@router.get("")
async def hello():
    return {"message": "Hello, World!"}
