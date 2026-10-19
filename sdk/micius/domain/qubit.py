from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Qubit:
    id: str
    owner: str

    @classmethod
    def from_dict(cls, data: dict) -> Qubit:
        return cls(id=str(data["id"]), owner=str(data["owner"]))
