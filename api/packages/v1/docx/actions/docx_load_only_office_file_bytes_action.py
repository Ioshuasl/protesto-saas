import logging
from urllib.parse import urlparse

import requests
from fastapi import HTTPException, status

from actions.env.env_config_loader import EnvConfigLoader
from packages.v1.docx.schemas.docx_schema import DOCXSchemaCallback

logger = logging.getLogger(__name__)


class DOCXLoadOnlyOfficeFileBytesAction:
    @staticmethod
    def execute(data: DOCXSchemaCallback) -> bytes:
        incoming_file_url = data.data.get("url")
        file_url = DOCXLoadOnlyOfficeFileBytesAction._resolve_file_url(incoming_file_url)

        if not file_url:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Callback do OnlyOffice sem URL de arquivo para download.",
            )

        logger.info(
            "OnlyOffice callback download iniciado",
            extra={"incoming_url": incoming_file_url, "resolved_url": file_url},
        )

        try:
            file_response = requests.get(file_url, timeout=30)
            file_response.raise_for_status()
        except requests.RequestException as exc:
            fallback_url = DOCXLoadOnlyOfficeFileBytesAction._resolve_cache_url_with_editor_base(
                incoming_file_url
            )
            if fallback_url and fallback_url != file_url:
                logger.warning(
                    "OnlyOffice download falhou na URL principal; tentando fallback",
                    extra={
                        "primary_url": file_url,
                        "fallback_url": fallback_url,
                        "error": str(exc),
                    },
                )
                try:
                    file_response = requests.get(fallback_url, timeout=30)
                    file_response.raise_for_status()
                    return file_response.content
                except requests.RequestException as fallback_exc:
                    raise HTTPException(
                        status_code=status.HTTP_502_BAD_GATEWAY,
                        detail=f"Falha ao baixar arquivo do OnlyOffice: {fallback_exc}",
                    )
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Falha ao baixar arquivo do OnlyOffice: {exc}",
            )

        return file_response.content

    @staticmethod
    def _resolve_file_url(file_url: str | None) -> str | None:
        if not file_url:
            return file_url

        env = EnvConfigLoader(env_file=".env")
        editor_url = getattr(env, "ORIUS_EDITOR", None)

        # Protocol-relative URL (e.g. //host/cache/...) -> assume HTTP.
        if file_url.startswith("//"):
            file_url = f"http:{file_url}"

        # Absolute URL from OnlyOffice cache may point to a host not reachable by API.
        # In that case, prefer ORIUS_EDITOR host while preserving the /cache path/query.
        if file_url.startswith("http://") or file_url.startswith("https://"):
            if editor_url and "/cache" in file_url:
                parsed_file = urlparse(file_url)
                parsed_editor = urlparse(editor_url)
                if parsed_editor.netloc and parsed_file.netloc != parsed_editor.netloc:
                    _, cache_path = file_url.split("/cache", 1)
                    return f"{editor_url.rstrip('/')}/cache{cache_path}"
            return file_url

        # Callback pode enviar URL relativa (/cache/...) em alguns cenarios.
        if file_url.startswith("/"):
            if not editor_url:
                return file_url
            return f"{editor_url.rstrip('/')}{file_url}"

        if file_url.startswith("cache/"):
            if not editor_url:
                return file_url
            return f"{editor_url.rstrip('/')}/{file_url}"

        if not editor_url or "/cache" not in file_url:
            return file_url

        _, cache_path = file_url.split("/cache", 1)
        return f"{editor_url.rstrip('/')}/cache{cache_path}"

    @staticmethod
    def _resolve_cache_url_with_editor_base(file_url: str | None) -> str | None:
        if not file_url or "/cache" not in file_url:
            return None

        env = EnvConfigLoader(env_file=".env")
        editor_url = getattr(env, "ORIUS_EDITOR", None)
        if not editor_url:
            return None

        _, cache_path = file_url.split("/cache", 1)
        return f"{editor_url.rstrip('/')}/cache{cache_path}"
