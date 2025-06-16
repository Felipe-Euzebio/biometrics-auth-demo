from fastapi import APIRouter, Form
from dependencies import AuthServiceDep
from schemas import LoginDto, RegisterDto

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register")
async def register(
    auth_service: AuthServiceDep,
    request: RegisterDto = Form(..., media_type="multipart/form-data")
):
    return await auth_service.register(request)

@router.post("/login")
async def login(
    auth_service: AuthServiceDep,
    request: LoginDto = Form(..., media_type="multipart/form-data"), 
):
    return await auth_service.login(request)
