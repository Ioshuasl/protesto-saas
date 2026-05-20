class GEDAllowedUploadTypesAction:
    # Lista explicita de tipos permitidos (facil de atualizar).
    ALLOWED_EXACT_MIME_TYPES = {
        "application/pdf",
    }
    # Prefixos aceitos para abrangencia de imagens.
    ALLOWED_MIME_PREFIXES = (
        "image/",
    )

    @staticmethod
    def normalize_mime(content_type: str | None) -> str:
        if not content_type:
            return ""
        return str(content_type).split(";", 1)[0].strip().lower()

    @staticmethod
    def is_allowed(content_type: str | None) -> bool:
        mime = GEDAllowedUploadTypesAction.normalize_mime(content_type)
        if not mime:
            return False
        if mime in GEDAllowedUploadTypesAction.ALLOWED_EXACT_MIME_TYPES:
            return True
        return any(
            mime.startswith(prefix)
            for prefix in GEDAllowedUploadTypesAction.ALLOWED_MIME_PREFIXES
        )

    @staticmethod
    def list_allowed() -> list[str]:
        exact = sorted(GEDAllowedUploadTypesAction.ALLOWED_EXACT_MIME_TYPES)
        prefixes = [f"{prefix}*" for prefix in GEDAllowedUploadTypesAction.ALLOWED_MIME_PREFIXES]
        return exact + prefixes
