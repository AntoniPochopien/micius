# Micius backend

FastAPI runtime for ownership-aware multi-party quantum sessions. Sessions live in Redis; circuits run against a shared Qiskit Aer statevector.

## Quick start

### Docker

From this directory:

```bash
docker compose up --build
```

API: [`http://127.0.0.1:8000`](http://127.0.0.1:8000) · docs: [`/docs`](http://127.0.0.1:8000/docs)

### Local

Requires Redis (`REDIS_URL`, default `redis://localhost:6379/0`).

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

uvicorn app.main:app --reload
```

Health: `GET /health`

---

## Architecture

Clean Architecture under `app/`:

```
app/
├── domain/           # Session, QuantumSystem, Job, Qubit
├── application/      # Use cases + Aer executor
├── infrastructure/   # Redis storage
└── presentation/     # FastAPI routes & schemas
```

Domain stays free of FastAPI / Aer details. The executor enforces ownership per instruction against a shared joint state.

### Core ideas

- **Sessions** — ephemeral workspaces with TTL
- **Quantum system** — `n` qubits → one `Statevector` of size `2ⁿ`, starting in `|0…0⟩`
- **Ownership** — instructions on foreign qubits are skipped (not rejected mid-circuit)
- **Jobs** — base64 QPY + `qubit_mapping` + `shots`; execution order = submission order
- **Transfer** — hand a qubit to another party; joint state stays intact

---

## API flow

Typical multi-party run:

| Step | Endpoint | What happens |
| --- | --- | --- |
| 1 | `POST /session` | Create a session |
| 2 | `GET /session/{id}` | Inspect session (qubits, jobs) |
| 3 | `POST /sessions/{id}/system` | Allocate qubits with owners |
| 4 | `POST /sessions/{id}/jobs` | Submit QPY circuit + mapping |
| 5 | `POST /sessions/{id}/qubits/{qid}/transfer` | *(optional)* change owner |
| 6 | `GET /sessions/{id}/jobs/execute` | Run queue → counts per caller |

For a higher-level client, see [`../sdk/README.md`](../sdk/README.md).
