import requests
from fastapi import HTTPException, status

from actions.env.env_config_loader import EnvConfigLoader
from packages.v1.docx.schemas.docx_schema import DOCXSchemaCallback


class DOCXLoadOnlyOfficeFileBytesAction:
    @staticmethod
    def execute(data: DOCXSchemaCallback) -> bytes:
        file_url = data.data.get("url")
        file_url = DOCXLoadOnlyOfficeFileBytesAction._resolve_file_url(file_url)

        if not file_url:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Callback do OnlyOffice sem URL de arquivo para download.",
            )

        try:
            file_response = requests.get(file_url, timeout=30)
            file_response.raise_for_status()
        except requests.RequestException as exc:
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
