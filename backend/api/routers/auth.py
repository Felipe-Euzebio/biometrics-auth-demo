from fastapi import APIRouter, Form, Request, Depends
from api.dependencies import AuthServiceDep, authx
from api.schemas import LoginDto, RegisterDto, AuthenticatedDto, RefreshTokenDto, NewAccessTokenDto, UserDto
from api.errors import HttpError

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post(
    "/register", 
    response_model=AuthenticatedDto,
    responses={
        400: {"model": HttpError},
        500: {"model": HttpError}
    }
)
async def register(
    auth_service: AuthServiceDep,
    request: RegisterDto = Form(..., media_type="multipart/form-data")
):
    return await auth_service.register(request)

@router.post(
    "/login", 
    response_model=AuthenticatedDto,
    responses={
        400: {"model": HttpError},
        401: {"model": HttpError},
        500: {"model": HttpError}
    }
)
async def login(
    auth_service: AuthServiceDep,
    request: LoginDto = Form(..., media_type="multipart/form-data"), 
):
    return await auth_service.login(request)

@router.post(
    "/refresh", 
    response_model=NewAccessTokenDto,
    responses={
        400: {"model": HttpError},
        401: {"model": HttpError},
        500: {"model": HttpError}
    }
)
async def refresh(
    auth_service: AuthServiceDep,
    request: Request,
    refresh_data: RefreshTokenDto = None
):
    return await auth_service.refresh(request, refresh_data)

@router.get(
    "/me", 
    response_model=UserDto, 
    dependencies=[Depends(authx.access_token_required)],
    responses={
        401: {"model": HttpError},
        404: {"model": HttpError},
        500: {"model": HttpError}
    }
)
async def get_current_user(
    auth_service: AuthServiceDep,
    request: Request,
):
    return await auth_service.get_current_user(request)
