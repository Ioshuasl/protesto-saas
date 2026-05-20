import asyncio
import json
import os
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping
from uuid import uuid4

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
try:
    from pymupdf import FileDataError as PyMuPdfFileDataError
except Exception:  # pragma: no cover
    PyMuPdfFileDataError = None

from actions.log.log import Log
from actions.system.exceptions import BusinessRuleException

VALIDATION_STATUS_CODE = 400
DEBUG_EXCEPTION_ENVS = {"dev", "development", "local"}


def _is_debug_enabled(app: Any, app_env: str | None) -> bool:
    app_state = getattr(app, "state", None)
    state_value = getattr(app_state, "debug_exception_details", None)
    if state_value is not None:
        return bool(state_value)

    effective_env = (app_env or os.getenv("APP_ENV", "development")).strip().lower()
    return effective_env in DEBUG_EXCEPTION_ENVS


def _get_request_id(request: Request) -> str:
    request_id = (
        request.headers.get("x-request-id")
        or getattr(request.state, "request_id", None)
        or str(uuid4())
    )
    request.state.request_id = request_id
    return request_id


def _sanitize_for_json(value: Any) -> Any:
    """Converte exceções em `ctx` do Pydantic (e similares) para tipos serializáveis."""
    if isinstance(value, BaseException):
        return str(value)
    if isinstance(value, Mapping):
        return {key: _sanitize_for_json(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_sanitize_for_json(item) for item in value]
    return value


def _build_error_response(
    *,
    status_code: int,
    error: str,
    message: str,
    request_id: str,
    details: Any = None,
) -> dict[str, Any]:
    return {
        "status": status_code,
        "error": error,
        "message": message,
        "details": details,
        "request_id": request_id,
    }


def _build_log_payload(
    *,
    request: Request,
    handler_name: str,
    response: dict[str, Any],
    exc: Exception,
    internal_details: Any = None,
) -> dict[str, Any]:
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "handler": handler_name,
        "exception_type": type(exc).__name__,
        "method": request.method,
        "path": request.url.path,
        "query_params": dict(request.query_params),
        "status_code": response["status"],
        "request_id": response["request_id"],
        "response": response,
        "internal_details": internal_details,
    }


async def _write_log(temp_dir: Path, file_name: str, payload: dict[str, Any]) -> None:
    await asyncio.to_thread(Log.register, payload, temp_dir / file_name)


def register_exception_handlers(
    app, *, temp_dir: str | Path = Path("storage") / "temp", app_env: str | None = None
) -> None:
    temp_dir = Path(temp_dir)
    debug_enabled = _is_debug_enabled(app, app_env)

    @app.exception_handler(BusinessRuleException)
    async def business_rule_exception_handler(
        request: Request, exc: BusinessRuleException
    ) -> JSONResponse:
        request_id = _get_request_id(request)
        response = _build_error_response(
            status_code=422,
            error="business_rule_error",
            message="Regra de negocio",
            details=exc.message,
            request_id=request_id,
        )
        log_payload = _build_log_payload(
            request=request,
            handler_name="business_rule_exception_handler",
            response=response,
            exc=exc,
            internal_details={"exception_message": exc.message},
        )

        await _write_log(temp_dir, "business_rule_exception_handler.json", log_payload)
        return JSONResponse(status_code=422, content=response)

    if PyMuPdfFileDataError is not None:
        @app.exception_handler(PyMuPdfFileDataError)
        async def pymupdf_file_data_error_handler(
            request: Request, exc: Exception
        ) -> JSONResponse:
            request_id = _get_request_id(request)
            response = _build_error_response(
                status_code=422,
                error="invalid_file_payload",
                message="Arquivo enviado invalido para processamento",
                details={"type": type(exc).__name__, "message": str(exc)},
                request_id=request_id,
            )
            log_payload = _build_log_payload(
                request=request,
                handler_name="pymupdf_file_data_error_handler",
                response=response,
                exc=exc,
                internal_details={"exception_message": str(exc)},
            )

            await _write_log(temp_dir, "pymupdf_file_data_error_handler.json", log_payload)
            return JSONResponse(status_code=422, content=response)

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(
        request: Request, exc: StarletteHTTPException
    ) -> JSONResponse:
        request_id = _get_request_id(request)
        message = exc.detail if isinstance(exc.detail, str) else "Erro HTTP"
        details = None if isinstance(exc.detail, str) else exc.detail
        response = _build_error_response(
            status_code=exc.status_code,
            error="http_error",
            message=message,
            details=details,
            request_id=request_id,
        )
        log_payload = _build_log_payload(
            request=request,
            handler_name="http_exception_handler",
            response=response,
            exc=exc,
            internal_details={"exception_detail": exc.detail},
        )

        await _write_log(temp_dir, "http_exception_handler.json", log_payload)
        return JSONResponse(status_code=exc.status_code, content=response)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        request_id = _get_request_id(request)
        errors = _sanitize_for_json(exc.errors())
        response = _build_error_response(
            status_code=VALIDATION_STATUS_CODE,
            error="validation_error",
            message="Erro de validacao",
            details=errors,
            request_id=request_id,
        )
        log_payload = _build_log_payload(
            request=request,
            handler_name="validation_exception_handler",
            response=response,
            exc=exc,
            internal_details={"validation_errors": errors},
        )

        await _write_log(temp_dir, "validation_exception_handler.json", log_payload)
        return JSONResponse(status_code=VALIDATION_STATUS_CODE, content=response)

    @app.exception_handler(json.JSONDecodeError)
    async def json_decode_exception_handler(
        request: Request, exc: json.JSONDecodeError
    ) -> JSONResponse:
        request_id = _get_request_id(request)
        response = _build_error_response(
            status_code=422,
            error="invalid_json_payload",
            message="JSON invalido no corpo da requisicao",
            details={"type": type(exc).__name__, "message": str(exc)},
            request_id=request_id,
        )
        log_payload = _build_log_payload(
            request=request,
            handler_name="json_decode_exception_handler",
            response=response,
            exc=exc,
            internal_details={"exception_message": str(exc)},
        )

        await _write_log(temp_dir, "json_decode_exception_handler.json", log_payload)
        return JSONResponse(status_code=422, content=response)

    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        request_id = _get_request_id(request)
        response_details = None
        if debug_enabled:
            response_details = {
                "type": type(exc).__name__,
                "message": str(exc),
            }

        response = _build_error_response(
            status_code=500,
            error="internal_server_error",
            message="Erro interno do servidor",
            details=response_details,
            request_id=request_id,
        )
        log_payload = _build_log_payload(
            request=request,
            handler_name="global_exception_handler",
            response=response,
            exc=exc,
            internal_details={
                "exception_message": str(exc),
                "traceback": "".join(
                    traceback.format_exception(type(exc), exc, exc.__traceback__)
                ),
            },
        )

        await _write_log(temp_dir, "global_exception_handler.json", log_payload)
        return JSONResponse(status_code=500, content=response)
