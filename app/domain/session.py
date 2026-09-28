from app.domain.quantum_system import QuantumSystem


class Session:

    def __init__(self, id: str, ttl: int = 30):
        self.id = id
        self.ttl = ttl  # seconds
        self.systems: list[QuantumSystem] = []
