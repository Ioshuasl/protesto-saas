# services/session_service.py
from fastapi import Request


class SessionService:
    def __init__(self, request: Request):
        self._session = request.session

    def set(self, k, v):
        self._session[k] = v

    def get(self, k, d=None):
        return self._session.get(k, d)

    def clear(self):
        self._session.clear()
