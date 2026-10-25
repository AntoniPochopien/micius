import uuid


class User:
    def __init__(self, username: str, hashed_password: str, id: str | None = None):
        self.id = id or str(uuid.uuid4())
        self.username = username
        self.hashed_password = hashed_password
