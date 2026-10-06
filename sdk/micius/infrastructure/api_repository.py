from __future__ import annotations

from typing import Any

import httpx

from micius.domain.failure import Failure


class ApiRepository:
    def __init__(self, base_url: str, *, timeout: float = 30.0):
        self._http = httpx.Client(base_url=base_url.rstrip("/"), timeout=timeout)

    def health(self) -> bool:
        self._request("GET", "/health")
        return True

    def create_session(self) -> dict[str, Any]:
        return self._request("POST", "/session")

    def get_session(self, session_id: str) -> dict[str, Any]:
        return self._request("GET", f"/session/{session_id}")

    def create_system(
        self,
        session_id: str,
        qubits: list[dict[str, str]],
    ) -> dict[str, Any]:
        return self._request(
            "POST",
            f"/sessions/{session_id}/system",
            json={"qubits": qubits},
        )

    def transfer_qubit(
        self,
        session_id: str,
        qubit_id: str,
        new_owner: str,
    ) -> dict[str, Any]:
        return self._request(
            "POST",
            f"/sessions/{session_id}/qubits/{qubit_id}/transfer",
            json={"new_owner": new_owner},
        )

    def create_job(
        self,
        session_id: str,
        *,
        caller: str,
        circuit: str,
        qubit_mapping: dict[str, str],
        shots: int,
    ) -> dict[str, Any]:
        return self._request(
            "POST",
            f"/sessions/{session_id}/jobs",
            json={
                "caller": caller,
                "circuit": circuit,
                "qubit_mapping": qubit_mapping,
                "shots": shots,
            },
        )

    def execute_jobs(self, session_id: str) -> dict[str, Any]:
        return self._request("GET", f"/sessions/{session_id}/jobs/execute")

    def close(self) -> None:
        self._http.close()

    def _request(
        self,
        method: str,
        path: str,
        **kwargs: Any,
    ) -> dict[str, Any]:
        response = self._http.request(method, path, **kwargs)
        if response.is_error:
            raise Failure(response.status_code, _error_detail(response))
        return response.json()


def _error_detail(response: httpx.Response) -> str:
    try:
        body = response.json()
    except ValueError:
        return response.text or response.reason_phrase
    if isinstance(body, dict) and "detail" in body:
        return str(body["detail"])
    return str(body)
