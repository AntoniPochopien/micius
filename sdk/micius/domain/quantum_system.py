from __future__ import annotations

from dataclasses import dataclass

from micius.domain.qubit import Qubit


@dataclass(frozen=True)
class QuantumSystem:
    qubits: tuple[Qubit, ...]

    @classmethod
    def from_dict(cls, data: dict) -> QuantumSystem:
        qubits = tuple(Qubit.from_dict(item) for item in data.get("qubits", []))
        return cls(qubits=qubits)
