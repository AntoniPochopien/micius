from app.application.auth import AuthService
from app.infrastructure.storage_repository import StorageRepository

# DI
storage_repository = StorageRepository()
auth_service = AuthService(storage_repository)
