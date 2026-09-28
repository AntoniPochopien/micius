import uuid

class StorageRepository:
    def __init__(self):
        self.storage = {}

    def create_session(self):
        session_id = str(uuid.uuid4())
        self.storage[session_id] = session_id
        return session_id

    def get_session(self, session_id: str):
        return self.storage.get(session_id)