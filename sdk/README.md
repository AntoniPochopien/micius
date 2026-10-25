# Micius SDK

Qiskit client for the [Micius](../readme.md) multi-party quantum runtime. Submits circuits as QPY, manages session / system / jobs over HTTP.

Requires a running backend — see [`../backend/README.md`](../backend/README.md).

## Install

From the repo root:

```bash
pip install -e ./sdk
```

Python ≥ 3.11. Depends on `httpx` and `qiskit`.

---

## Quick start

```python
from qiskit import QuantumCircuit
from micius import MiciusClient

with MiciusClient("http://127.0.0.1:8000", caller="alice") as client:
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])

    client.sync(qc)             # create system (once) + queue job
    results = client.execute()  # counts keyed by caller
```

Join an existing session with `session_id=...` (system is assumed already created).

---

## Client API

| Method | Role |
| --- | --- |
| `sync(circuit)` | On first call: create system owned by `caller`. Always enqueue a job (`q0…qn` mapping, default shots). |
| `transfer(qubit, new_owner)` | Transfer by index (`0` → `q0`) or id (`"q0"`). |
| `measure(caller=None)` | Enqueue measure-only job for qubits owned by that caller. |
| `execute(measure=True)` | Optionally auto-measure owners missing a measure job, then run the queue. |
| `health()` | `GET /health` |
| `session_id` | Current session id |

Context manager closes the underlying HTTP client.

---

## Multi-party sketch

```python
with MiciusClient("http://127.0.0.1:8000", caller="alice") as alice:
    prep = QuantumCircuit(2)
    prep.h(0)
    prep.cx(0, 1)
    alice.sync(prep)
    alice.transfer(1, "bob")

    with MiciusClient(
        "http://127.0.0.1:8000",
        caller="bob",
        session_id=alice.session_id,
    ) as bob:
        results = bob.execute()  # measures remaining owners, then executes
```
