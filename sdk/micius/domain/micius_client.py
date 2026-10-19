from __future__ import annotations

import base64
import io

from qiskit import QuantumCircuit, qpy

from micius.domain.execute_result import ExecuteResult
from micius.domain.failure import Failure, SessionNotFound
from micius.domain.qubit import Qubit
from micius.infrastructure.api_repository import ApiRepository


class MiciusClient:
    def __init__(
        self,
        base_url: str,
        caller: str,
        *,
        session_id: str | None = None,
        timeout: float = 30.0,
        shots: int = 1024,
    ):
        self.api_repository = ApiRepository(base_url, timeout=timeout)
        self._caller = caller
        self._shots = shots
        if session_id is None:
            session = self.api_repository.create_session()
            self._session_id = session.id
            self._system_created = False
        else:
            try:
                self.api_repository.get_session(session_id)
            except Failure as exc:
                self.api_repository.close()
                if exc.status_code == 404:
                    raise SessionNotFound(session_id) from exc
                raise
            self._session_id = session_id
            self._system_created = True

    @property
    def session_id(self) -> str:
        return self._session_id

    def sync(self, circuit: QuantumCircuit) -> None:
        if not self._system_created:
            qubits = []
            for i in range(circuit.num_qubits):
                qubits.append(Qubit(id=f"q{i}", owner=self._caller))
            self.api_repository.create_system(self._session_id, qubits)
            self._system_created = True

        qubit_mapping = {}
        for i in range(circuit.num_qubits):
            qubit_mapping[i] = f"q{i}"
        self.api_repository.create_job(
            self._session_id,
            caller=self._caller,
            circuit=_encode_circuit(circuit),
            qubit_mapping=qubit_mapping,
            shots=self._shots,
        )

    def transfer(self, qubit: int | str, new_owner: str) -> None:
        qubit_id = f"q{qubit}" if isinstance(qubit, int) else qubit
        self.api_repository.transfer_qubit(self._session_id, qubit_id, new_owner)

    def measure(self, caller: str | None = None) -> None:
        """Enqueue a measurement job for qubits currently owned by caller."""
        owner = caller if caller is not None else self._caller
        session = self.api_repository.get_session(self._session_id)
        owned_ids = []
        for qubit in session.qubits:
            if qubit.owner == owner:
                owned_ids.append(qubit.id)
        if len(owned_ids) == 0:
            return

        circuit = QuantumCircuit(len(owned_ids), len(owned_ids))
        for index in range(len(owned_ids)):
            circuit.measure(index, index)

        qubit_mapping = {}
        for i in range(len(owned_ids)):
            qubit_mapping[i] = owned_ids[i]
        self.api_repository.create_job(
            self._session_id,
            caller=owner,
            circuit=_encode_circuit(circuit),
            qubit_mapping=qubit_mapping,
            shots=self._shots,
        )

    def execute(self, *, measure: bool = True) -> ExecuteResult:
        session = self.api_repository.get_session(self._session_id)
        if measure and not session.executed:
            measured_owners = set()
            for job in session.jobs:
                if job.has_measure:
                    measured_owners.add(job.caller)

            owners = set()
            for qubit in session.qubits:
                owners.add(qubit.owner)

            for owner in sorted(owners - measured_owners):
                self.measure(caller=owner)

        return self.api_repository.execute_jobs(
            self._session_id,
            caller=self._caller,
        )

    def health(self) -> bool:
        return self.api_repository.health()

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
