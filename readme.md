# Micius

**A multi-party quantum runtime with ownership-aware qubit control.**

Named after the *Micius* quantum satellite - the first craft to demonstrate space-to-ground quantum key distribution - this service lets multiple callers share one entangled system, own individual qubits, transfer them, and run circuits against a joint statevector without stepping on each other’s wire.

```
┌─────────────┐     circuit (QPY)      ┌──────────────────┐
│  Caller A   │ ─────────────────────► │      MICIUS      │
└─────────────┘                        │  shared system   │
┌─────────────┐     qubit transfer     │   + ownership    │──► counts / caller
│  Caller B   │ ─────────────────────► │                  │
└─────────────┘                        └──────────────────┘
```

---

## Why it exists

Most quantum simulators assume a single owner of the whole register. Real protocols don’t.

Micius models a **shared quantum system** where every qubit has an owner, jobs only act on owned wires, the global statevector evolves in place across jobs, and ownership can move mid-session via transfer.

---

## Stack

| Layer | Tech |
| --- | --- |
| API | **FastAPI** + Redis |
| Circuits | **Qiskit** (QPY over the wire) |
| Simulation | **Qiskit Aer** statevector |
| Client | pip package `micius` |

---

## Repo

```
micius/
├── backend/   # FastAPI runtime
├── sdk/       # Qiskit client
└── readme.md
```

- **[Backend](backend/README.md)** — run the API, architecture, endpoints
- **[SDK](sdk/README.md)** — install the client and submit circuits

---

## Status

Experimental runtime for ownership-aware multi-party quantum simulation.

Built for protocols that need more than “one circuit, one owner.”

---

<p align="center">
  <sub>Micius · shared quantum systems with intent</sub>
</p>
