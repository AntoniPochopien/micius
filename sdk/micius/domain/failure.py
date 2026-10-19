class Failure(Exception):
    def __init__(self, status_code: int, detail: str):
        self.status_code = status_code
        self.detail = detail
        super().__init__(f"{status_code}: {detail}")


class SessionNotFound(Failure):
    def __init__(self, session_id: str):
        super().__init__(404, f"Session '{session_id}' not found")
