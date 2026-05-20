import unicodedata
from typing import Optional

from packages.v1.administrativo.actions.g_gramatica.g_gramatica_get_by_palavra_action import (
    GGramaticaGetByPalavraAction,
)
from packages.v1.administrativo.schemas.g_gramatica_schema import (
    GGramaticaPalavraSchema,
)
from packages.v1.resolver.services.gramatica.resolver_gramatica_inferencia_service import (
    infer_numero_genero,
)
from packages.v1.resolver.services.gramatica.resolver_gramatica_tag_parser_service import (
    parse_gram_tag,
)


class ResolverGramaticaQualifierService:
    def __init__(self):
        self.action = GGramaticaGetByPalavraAction()
        self._cache_por_palavra = {}

    def execute(self, raw_tag: str, ctx: Optional[dict]) -> Optional[str]:
        parsed = parse_gram_tag(raw_tag)
        if not parsed:
            return None

        palavra, tipo = parsed
        contexto = ctx or {}

        role_ctx = {
            "1": contexto.get("outorgante"),
            "2": contexto.get("outorgado"),
            "3": contexto.get("imoveis"),
        }.get(tipo)

        if not role_ctx:
            return None

        inferido = self._infer_for_tipo(tipo, role_ctx)
        if not inferido:
            return None

        numero, genero = inferido

        row = self._buscar_palavra(palavra)

        if not row:
            return None

        sufixo_coluna = f"SUFIXO_{genero}{numero}"
        prefixo = self._get_row_value(row, "PREFIXO", "prefixo") or ""
        sufixo = self._get_row_value(row, sufixo_coluna, sufixo_coluna.lower()) or ""
        result = f"{prefixo}{sufixo}"
        if not str(result).strip():
            return None

        return self._preserve_case(palavra, result)

    def _buscar_palavra(self, palavra: str):
        palavra_normalizada = self._to_plain_text(palavra)
        if not palavra_normalizada:
            return None

        if palavra_normalizada in self._cache_por_palavra:
            return self._cache_por_palavra[palavra_normalizada]

        row = self.action.execute(
            GGramaticaPalavraSchema(
                palavra=palavra_normalizada,
            )
        )
        self._cache_por_palavra[palavra_normalizada] = row
        return row

    def _preserve_case(self, source: str, result: str) -> str:
        if not result:
            return result

        if source.isupper():
            return result.upper()

        if source.islower():
            return result.lower()

        if source[:1].isupper() and source[1:].islower():
            return result[:1].upper() + result[1:].lower()

        return result

    def _get_row_value(self, row: dict, *keys: str):
        for key in keys:
            value = row.get(key)
            if value is not None:
                return str(value).strip()
        return None

    def _infer_for_tipo(self, tipo: str, role_ctx: dict):
        if tipo == "3":
            quantity = role_ctx.get("quantity") if isinstance(role_ctx, dict) else None
            if not isinstance(quantity, int) or quantity <= 0:
                return None
            numero = "S" if quantity == 1 else "P"
            return numero, "M"
        return infer_numero_genero(role_ctx)

    def _to_plain_text(self, value: str) -> str:
        raw = unicodedata.normalize("NFKD", str(value or ""))
        chars = []
        for char in raw:
            if unicodedata.combining(char):
                continue

            category = unicodedata.category(char)
            if category.startswith("C"):
                continue

            if category.startswith("Z"):
                chars.append(" ")
                continue

            chars.append(char)

        return " ".join("".join(chars).split()).upper()
