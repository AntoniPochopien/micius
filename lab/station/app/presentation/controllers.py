from fastapi import APIRouter, HTTPException, Request

from app.dependencies import auth_service, storage_repository
from app.presentation.schema import (
    LoginRequest,
    RefreshRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)

router = APIRouter()


@router.get("/health")
def health():
    if not storage_repository.ping():
        raise HTTPException(status_code=503, detail="Redis unavailable")
    return {"status": "ok"}


@router.post("/register", response_model=TokenResponse)
def register(request: RegisterRequest):
    try:
        access_token, refresh_token = auth_service.register(
            request.username,
            request.password,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/token", response_model=TokenResponse)
def login(request: LoginRequest):
    try:
        access_token, refresh_token = auth_service.login(
            request.username,
            request.password,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/token/refresh", response_model=TokenResponse)
def refresh(request: RefreshRequest):
    try:
        access_token, refresh_token = auth_service.refresh(request.refresh_token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e)) from e
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.get("/me", response_model=UserResponse)
def me(request: Request):
    user = request.state.user
    return UserResponse(id=user.id, username=user.username)
