from fastapi import APIRouter, Form, Request, Depends, Response
from api.dependencies import AuthServiceDep, authx
from api.schemas import (
    LoginDto, 
    RegisterDto, 
    AuthenticatedDto, 
    RefreshTokenDto, 
    NewAccessTokenDto, 
    UserDto,
    HttpError,
    ValidationError,
    InternalServerError
)
from api.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post(
    "/register", 
    response_model=AuthenticatedDto,
    responses={
        400: {"model": HttpError},
        422: {"model": ValidationError},
        500: {"model": InternalServerError}
    }
)
async def register(
    response: Response,
    auth_service: AuthServiceDep,
    request: RegisterDto = Form(..., media_type="multipart/form-data")
):
    result = await auth_service.register(request)
    response.set_cookie(
        key=settings.cookie_name,
        value=result.refresh_token,
        httponly=settings.cookie_http_only,
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite,
        max_age=settings.cookie_max_age,
        path=settings.cookie_path
    )
    return result


@router.post(
    "/login", 
    response_model=AuthenticatedDto,
    responses={
        400: {"model": HttpError},
        401: {"model": HttpError},
        422: {"model": ValidationError},
        500: {"model": InternalServerError}
    }
)
async def login(
    response: Response,
    auth_service: AuthServiceDep,
    request: LoginDto = Form(..., media_type="multipart/form-data"), 
):
    result = await auth_service.login(request)
    response.set_cookie(
        key=settings.cookie_name,
        value=result.refresh_token,
        httponly=settings.cookie_http_only,
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite,
        max_age=settings.cookie_max_age,
        path=settings.cookie_path
    )
    return result


@router.post(
    "/refresh", 
    response_model=NewAccessTokenDto,
    responses={
        400: {"model": HttpError},
        401: {"model": HttpError},
        422: {"model": ValidationError},
        500: {"model": InternalServerError}
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
        422: {"model": ValidationError},
        500: {"model": InternalServerError}
    }
)
async def get_current_user(
    auth_service: AuthServiceDep,
    request: Request,
):
    return await auth_service.get_current_user(request)
