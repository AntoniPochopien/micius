from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Job:
    id: str
    caller: str
    has_measure: bool = False
    qubit_mapping: dict[int, str] | None = None
    shots: int | None = None

    @classmethod
    def from_dict(cls, data: dict) -> Job:
        raw_mapping = data.get("qubit_mapping")
        qubit_mapping = None
        if raw_mapping is not None:
            qubit_mapping = {int(key): str(value) for key, value in raw_mapping.items()}
        shots = data.get("shots")
        return cls(
            id=str(data["id"]),
            caller=str(data["caller"]),
            has_measure=bool(data.get("has_measure", False)),
            qubit_mapping=qubit_mapping,
            shots=int(shots) if shots is not None else None,
        )
