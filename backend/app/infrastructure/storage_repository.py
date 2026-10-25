import os
import pickle
import time
import uuid

import redis

from app.domain.job import Job
from app.domain.qubit import Qubit
from app.domain.quantum_system import QuantumSystem
from app.domain.session import Session

SESSION_KEY_PREFIX = "session:"


class StorageRepository:
    def __init__(self, redis_url: str):
        self._redis = redis.Redis.from_url(redis_url, decode_responses=False)

    def ping(self) -> bool:
        try:
            return bool(self._redis.ping())
        except redis.RedisError:
            return False

    def _key(self, session_id: str) -> str:
        return f"{SESSION_KEY_PREFIX}{session_id}"

    def _remaining_ttl(self, session: Session) -> int:
        return session.ttl - (int(time.time()) - session.created_at)

    def _load(self, session_id: str) -> Session | None:
        raw = self._redis.get(self._key(session_id))
        if raw is None:
            return None
        session: Session = pickle.loads(raw)
        if session.is_expired():
            self._redis.delete(self._key(session_id))
            return None
        return session

    def _save(self, session: Session) -> None:
        remaining = self._remaining_ttl(session)
        if remaining <= 0:
            self._redis.delete(self._key(session.id))
            return
        self._redis.set(self._key(session.id), pickle.dumps(session), ex=remaining)

    def save_session(self, session: Session) -> None:
        self._save(session)

    def create_session(self) -> Session:
        session_id = str(uuid.uuid4())
        session = Session(session_id)
        self._save(session)
        return session

    def get_session(self, session_id: str) -> Session | None:
        return self._load(session_id)

    def create_quantum_system(self, session_id: str, qubits: list[Qubit]) -> QuantumSystem | None:
        session = self.get_session(session_id)
        if session is None:
            return None

        system_id = str(uuid.uuid4())
        system = QuantumSystem(system_id, qubits)
        session.system = system
        self._save(session)
        return system

    def get_quantum_system(self, session_id: str) -> QuantumSystem | None:
        session = self.get_session(session_id)
        if session is None:
            return None
        return session.system

    def transfer_qubit(self, session_id: str, qubit_id: str, new_owner: str) -> Qubit | None:
        session = self.get_session(session_id)
        if session is None or session.system is None:
            return None
        for qubit in session.system.qubits:
            if qubit.id == qubit_id:
                qubit.owner = new_owner
                self._save(session)
                return qubit
        return None

    def create_job(self, session_id: str, job: Job) -> Job | None:
        session = self.get_session(session_id)
        if session is None or session.system is None:
            return None

        qubits_by_id = {qubit.id: qubit for qubit in session.system.qubits}
        owned_qubits_mapping: dict[int, str] = {}
        for circuit_index, qubit_id in job.qubit_mapping.items():
            qubit = qubits_by_id.get(qubit_id)
            if qubit is None:
                continue
            if qubit.owner != job.caller:
                continue
            owned_qubits_mapping[int(circuit_index)] = qubit_id

        job.owned_qubits_mapping = owned_qubits_mapping
        session.jobs.append(job)
        session.results = None
        self._save(session)
        return job
