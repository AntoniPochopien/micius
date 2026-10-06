from __future__ import annotations

import base64
import io
from typing import Any

from qiskit import QuantumCircuit, qpy

from micius.infrastructure.api_repository import ApiRepository


class MiciusClient:
    def __init__(self, base_url: str, *, timeout: float = 30.0):
        self.api_repository = ApiRepository(base_url, timeout=timeout)

    def health(self) -> bool:
        return self.api_repository.health()

    def create_session(self) -> dict[str, Any]:
        return self.api_repository.create_session()

    def get_session(self, session_id: str) -> dict[str, Any]:
        return self.api_repository.get_session(session_id)

    def create_system(
        self,
        session_id: str,
        qubits: list[dict[str, str]],
    ) -> dict[str, Any]:
        """Allocate a joint register. Each qubit: ``{"id": "...", "owner": "..."}``."""
        return self.api_repository.create_system(session_id, qubits)

    def transfer_qubit(
        self,
        session_id: str,
        qubit_id: str,
        new_owner: str,
    ) -> dict[str, Any]:
        return self.api_repository.transfer_qubit(session_id, qubit_id, new_owner)

    def submit_job(
        self,
        session_id: str,
        *,
        caller: str,
        circuit: QuantumCircuit,
        qubit_mapping: dict[int, str],
        shots: int,
    ) -> dict[str, Any]:
        """Queue a Qiskit circuit; SDK handles QPY + base64 for the wire format."""
        return self.api_repository.create_job(
            session_id,
            caller=caller,
            circuit=_encode_circuit(circuit),
            qubit_mapping={str(k): v for k, v in qubit_mapping.items()},
            shots=shots,
        )

    def execute(self, session_id: str) -> dict[str, dict[str, int]]:
        """Run the session job queue. Returns counts keyed by caller."""
        payload = self.api_repository.execute_jobs(session_id)
        return payload["results"]

    def close(self) -> None:
        self.api_repository.close()

    def __enter__(self) -> MiciusClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()


def _encode_circuit(circuit: QuantumCircuit) -> str:
    buffer = io.BytesIO()
    qpy.dump(circuit, buffer)
    return base64.b64encode(buffer.getvalue()).decode("ascii")
