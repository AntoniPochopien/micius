from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ExecuteResult:
    caller: str
    counts: dict[str, int]

    @classmethod
    def from_dict(cls, data: dict, *, caller: str) -> ExecuteResult:
        raw_results = data.get("results", {})
        raw_counts = raw_results.get(caller, {})
        counts = {str(bitstring): int(count) for bitstring, count in raw_counts.items()}
        return cls(caller=caller, counts=counts)

    def get(self, bitstring: str, default: int = 0) -> int:
        return self.counts.get(bitstring, default)

    def __getitem__(self, bitstring: str) -> int:
        return self.counts[bitstring]

    def __iter__(self):
        return iter(self.counts.items())

    def __len__(self) -> int:
        return len(self.counts)
