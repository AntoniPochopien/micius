from __future__ import annotations

from dataclasses import dataclass

from micius.domain.job import Job
from micius.domain.qubit import Qubit


@dataclass(frozen=True)
class Session:
    id: str
    qubits: tuple[Qubit, ...] = ()
    jobs: tuple[Job, ...] = ()
    executed: bool = False

    @classmethod
    def from_dict(cls, data: dict) -> Session:
        qubits = tuple(Qubit.from_dict(item) for item in data.get("qubits", []))
        jobs = tuple(Job.from_dict(item) for item in data.get("jobs", []))
        return cls(
            id=str(data["id"]),
            qubits=qubits,
            jobs=jobs,
            executed=bool(data.get("executed", False)),
        )
