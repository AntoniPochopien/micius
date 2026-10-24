import time

from app.domain.job import Job
from app.domain.quantum_system import QuantumSystem


class Session:
    SESSION_DEFAULT_TTL = 24 * 60 * 60 # 24 hours
    def __init__(self, id: str, ttl: int = SESSION_DEFAULT_TTL):
        self.id = id
        self.ttl = ttl  # seconds
        self.created_at = int(time.time())
        self.system: QuantumSystem | None = None
        self.jobs: list[Job] = []
        self.results: dict[str, dict[str, int]] | None = None

    def is_expired(self) -> bool:
        return int(time.time()) - self.created_at > self.ttl
