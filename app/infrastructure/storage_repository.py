import uuid
from app.domain.session import Session

class StorageRepository:
    def __init__(self):
        self.storage = {}

    def create_session(self) -> Session:
        session_id = str(uuid.uuid4())
        session = Session(session_id)
        self.storage[session_id] = session
        return session

    def get_session(self, session_id: str) -> Session:
        return self.storage[session_id]