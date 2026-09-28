from fastapi import FastAPI

from app.presentation.controllers import router

app = FastAPI()
app.include_router(router)
