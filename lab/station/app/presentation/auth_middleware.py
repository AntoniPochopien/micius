from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app.dependencies import auth_service

WHITELIST = {
    "/health",
    "/register",
    "/token",
    "/token/refresh",
}


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in WHITELIST:
            return await call_next(request)

        authorization = request.headers.get("Authorization")
        if authorization is None or not authorization.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"detail": "Unauthorized"})

        token = authorization.removeprefix("Bearer ").strip()
        user = auth_service.get_user_by_token(token)
        if user is None:
            return JSONResponse(status_code=401, content={"detail": "Invalid or expired token"})

        request.state.user = user
        return await call_next(request)
