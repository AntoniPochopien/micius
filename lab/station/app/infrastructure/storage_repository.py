import os
import pickle
import secrets

import redis

from app.domain.user import User

USER_KEY_PREFIX = "user:"
ACCESS_TOKEN_KEY_PREFIX = "access:"
REFRESH_TOKEN_KEY_PREFIX = "refresh:"
ACCESS_TOKEN_TTL_SECONDS = 60 * 15
REFRESH_TOKEN_TTL_SECONDS = 60 * 60 * 24 * 7


class StorageRepository:
    _instance: "StorageRepository | None" = None

    def __new__(cls, redis_url: str | None = None):
        if cls._instance is None:
            instance = super().__new__(cls)
            url = redis_url or os.getenv("REDIS_URL", "redis://localhost:6379/0")
            instance._redis = redis.Redis.from_url(url, decode_responses=False)
            cls._instance = instance
        return cls._instance

    def ping(self) -> bool:
        try:
            return bool(self._redis.ping())
        except redis.RedisError:
            return False

    def get_user(self, username: str) -> User | None:
        raw = self._redis.get(f"{USER_KEY_PREFIX}{username}")
        if raw is None:
            return None
        return pickle.loads(raw)

    def save_user(self, user: User) -> None:
        self._redis.set(f"{USER_KEY_PREFIX}{user.username}", pickle.dumps(user))

    def create_token_pair(self, username: str) -> tuple[str, str]:
        access_token = secrets.token_urlsafe(32)
        refresh_token = secrets.token_urlsafe(32)
        self._redis.set(
            f"{ACCESS_TOKEN_KEY_PREFIX}{access_token}",
            username.encode(),
            ex=ACCESS_TOKEN_TTL_SECONDS,
        )
        self._redis.set(
            f"{REFRESH_TOKEN_KEY_PREFIX}{refresh_token}",
            username.encode(),
            ex=REFRESH_TOKEN_TTL_SECONDS,
        )
        return access_token, refresh_token

    def get_username_by_access_token(self, token: str) -> str | None:
        raw = self._redis.get(f"{ACCESS_TOKEN_KEY_PREFIX}{token}")
        if raw is None:
            return None
        return raw.decode()

    def get_username_by_refresh_token(self, token: str) -> str | None:
        raw = self._redis.get(f"{REFRESH_TOKEN_KEY_PREFIX}{token}")
        if raw is None:
            return None
        return raw.decode()

    def revoke_refresh_token(self, token: str) -> None:
        self._redis.delete(f"{REFRESH_TOKEN_KEY_PREFIX}{token}")
