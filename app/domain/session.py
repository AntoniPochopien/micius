import time

from app.domain.quantum_system import QuantumSystem


class Session:

    def __init__(self, id: str, ttl: int = 30):
        self.id = id
        self.ttl = ttl  # seconds
        self.created_at = int(time.time())
        self.system: QuantumSystem | None = None

    def is_expired(self) -> bool:
        return int(time.time()) - self.created_at > self.ttl
