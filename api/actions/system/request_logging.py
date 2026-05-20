import asyncio
from pathlib import Path
from types import SimpleNamespace
from typing import Callable

from fastapi import FastAPI, Request, Response

from actions.log.log import Log

SENSITIVE_HEADERS = {"authorization", "cookie", "set-cookie", "x-api-key"}


def _sanitize_headers(headers: dict[str, str]) -> dict[str, str]:
    sanitized: dict[str, str] = {}

    for key, value in headers.items():
        sanitized[key] = "[REDACTED]" if key.lower() in SENSITIVE_HEADERS else value

    return sanitized


def configure_request_logging(app: FastAPI, app_config: SimpleNamespace) -> None:
    log = Log()
    file_path = Path(app_config.log.request.path) / app_config.log.request.name

    @app.middleware("http")
    async def log_request(
        request: Request, call_next: Callable[..., Response]
    ) -> Response:
        log_data = {
            "method": request.method,
            "url": str(request.url),
            "headers": _sanitize_headers(dict(request.headers)),
        }

        await asyncio.to_thread(log.register, log_data, file_path)
        return await call_next(request)
