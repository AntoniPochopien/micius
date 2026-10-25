from fastapi import FastAPI

from app.presentation.auth_middleware import AuthMiddleware
from app.presentation.controllers import router

app = FastAPI()
app.add_middleware(AuthMiddleware)
app.include_router(router)
