# Micius

**A multi-party quantum runtime with ownership-aware qubit control.**

Named after the *Micius* quantum satellite - the first craft to demonstrate space-to-ground quantum key distribution - this service lets multiple callers share one entangled system, own individual qubits, transfer them, and run circuits against a joint statevector without stepping on each other’s wire.

```
┌─────────────┐     circuit (QPY)      ┌──────────────────┐
│  Caller A   │ ─────────────────────► │                  │
└─────────────┘                        │     MICIUS       │
┌─────────────┐     qubit transfer     │  shared system   │──► counts / caller
│  Caller B   │ ─────────────────────► │  + ownership     │
└─────────────┘                        └──────────────────┘
```

---

## Why it exists

Most quantum simulators assume a single owner of the whole register. Real protocols don’t.

Micius models a **shared quantum system** where:

- every qubit has an **owner**
- jobs only apply gates / measurements on qubits the caller owns
- the global statevector **evolves in place** across jobs
- ownership can move mid-session via transfer

Think: collaborative Bell experiments, delegated measurement, or multi-party protocol sketches - without hand-rolling state plumbing.

---

## Stack

| Layer | Tech |
| --- | --- |
| API | **FastAPI** |
| Circuits | **Qiskit** (QPY over the wire) |
| Simulation | **Qiskit Aer** statevector |
| Architecture | Clean Architecture - `domain` · `application` · `infrastructure` · `presentation` |

---

## Core ideas

### Sessions
Ephemeral workspaces with TTL. Create one, attach a system, queue jobs, execute.

### Quantum system
A joint register: `n` qubits → one `Statevector` of size `2ⁿ`, starting in `|0…0⟩`.

### Ownership
Each qubit is tagged with an `owner`. Instructions targeting foreign qubits are skipped - not rejected mid-circuit - so partial ownership still produces a meaningful evolution.

### Jobs
Submitted as base64-encoded **QPY** circuits plus a `qubit_mapping` (`circuit index → qubit id`) and `shots`. Execution order = submission order. Unitaries evolve state; measurements collapse it and return counts keyed by caller.

### Transfer
Hand a qubit to another party mid-session. Ownership updates; the joint state stays intact.

---

## Architecture

```
micius/
├── backend/          # FastAPI runtime
│   └── app/
│       ├── domain/
│       ├── application/
│       ├── infrastructure/
│       └── presentation/
├── sdk/              # pip package `micius` (Qiskit client)
│   └── micius/
└── readme.md
```

Domain stays free of FastAPI / Aer details. The executor enforces ownership per instruction against a shared joint state.

---

## Quick start

### Backend

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt

cd backend
uvicorn app.main:app --reload
```

Open docs at [`http://127.0.0.1:8000/docs`](http://127.0.0.1:8000/docs).

### SDK

```bash
pip install -e ./sdk
```

```python
from qiskit import QuantumCircuit
from micius import MiciusClient

with MiciusClient("http://127.0.0.1:8000") as client:
    session = client.create_session()
    sid = session["id"]

    client.create_system(
        sid,
        [{"id": "q0", "owner": "alice"}, {"id": "q1", "owner": "bob"}],
    )

    qc = QuantumCircuit(1, 1)
    qc.h(0)
    qc.measure(0, 0)

    client.submit_job(
        sid,
        caller="alice",
        circuit=qc,
        qubit_mapping={0: "q0"},
        shots=1024,
    )

    results = client.execute(sid)  # counts per caller
```

---

## API flow

Typical multi-party run:

| Step | Endpoint | What happens |
| --- | --- | --- |
| 1 | `POST /session` | Create a session |
| 2 | `POST /sessions/{id}/system` | Allocate qubits with owners |
| 3 | `POST /sessions/{id}/jobs` | Submit QPY circuit + mapping |
| 4 | `POST /sessions/{id}/qubits/{qid}/transfer` | *(optional)* change owner |
| 5 | `GET /sessions/{id}/jobs/execute` | Run queue → counts per caller |

Health check: `GET /health`

## Status

Experimental runtime for ownership-aware multi-party quantum simulation. In-memory sessions, Aer-backed statevector, FastAPI surface.

Built for protocols that need more than “one circuit, one owner.”

---

<p align="center">
  <sub>Micius · shared quantum systems with intent</sub>
</p>
