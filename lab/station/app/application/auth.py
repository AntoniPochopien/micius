import hashlib
import hmac
import secrets

from app.domain.user import User
from app.infrastructure.storage_repository import StorageRepository


class AuthService:
    def __init__(self, storage: StorageRepository):
        self._storage = storage

    def register(self, username: str, password: str) -> tuple[str, str]:
        if self._storage.get_user(username) is not None:
            raise ValueError("Username already taken")
        user = User(username=username, hashed_password=self._hash_password(password))
        self._storage.save_user(user)
        return self._storage.create_token_pair(user.username)

    def login(self, username: str, password: str) -> tuple[str, str]:
        user = self._storage.get_user(username)
        if user is None or not self._verify_password(password, user.hashed_password):
            raise ValueError("Incorrect username or password")
        return self._storage.create_token_pair(user.username)

    def refresh(self, refresh_token: str) -> tuple[str, str]:
        username = self._storage.get_username_by_refresh_token(refresh_token)
        if username is None:
            raise ValueError("Invalid or expired refresh token")
        self._storage.revoke_refresh_token(refresh_token)
        return self._storage.create_token_pair(username)

    def get_user_by_token(self, token: str) -> User | None:
        username = self._storage.get_username_by_access_token(token)
        if username is None:
            return None
        return self._storage.get_user(username)

    def _hash_password(password: str, salt: str | None = None) -> str:
        salt = salt or secrets.token_hex(16)
        digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode(),
            salt.encode(),
            100_000,
        )
        return f"{salt}${digest.hex()}"

    def _verify_password(password: str, hashed_password: str) -> bool:
        salt, _, _ = hashed_password.partition("$")
        if not salt:
            return False
        candidate = AuthService._hash_password(password, salt)
        return hmac.compare_digest(hashed_password, candidate)
