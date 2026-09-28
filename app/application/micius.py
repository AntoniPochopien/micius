from app.infrastructure.storage_repository import StorageRepository

class Micius:
    def __init__(self, storage_repository: StorageRepository):
        self.storage_repository = storage_repository

    def create_session(self):
        self.storage_repository.create_session()

    def get_session(self, session_id: str):
        return self.storage_repository.get_session(session_id)