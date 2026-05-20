import re
from fastapi import HTTPException, status


class DOCXRTFExtractorAction:
    """
    Extrator de finalizacao orientado a RTF (bookmarks no texto RTF).
    Mapeamento:
      1 -> FINALIZACAO_LIVRO
      2 -> FINALIZACAO_TRASLADO
    """

    _BOOKMARK_BY_TIPO = {
        1: "FINALIZACAO_LIVRO",
        2: "FINALIZACAO_TRASLADO",
    }

    _BOOKMARK_PATTERNS = {
        1: re.compile(
            r"\{\\\*\\bkmkstart\s+FINALIZACAO_LIVRO\}(.*?)\{\\\*\\bkmkend\s+FINALIZACAO_LIVRO\}",
            flags=re.DOTALL | re.IGNORECASE,
        ),
        2: re.compile(
            r"\{\\\*\\bkmkstart\s+FINALIZACAO_TRASLADO\}(.*?)\{\\\*\\bkmkend\s+FINALIZACAO_TRASLADO\}",
            flags=re.DOTALL | re.IGNORECASE,
        ),
    }

    def __init__(self, content: str):
        self.content = content

    def execute(self, tipo_finalizacao: int) -> str:
        tipo = self._parse_tipo(tipo_finalizacao)
        bookmark_tag = self._BOOKMARK_BY_TIPO[tipo]
        pattern = self._BOOKMARK_PATTERNS[tipo]

        match = pattern.search(self.content or "")
        if not match:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Bookmark '{bookmark_tag}' nao encontrado no texto de finalizacao.",
            )

        extracted = self._clean_rtf(match.group(1))
        if not extracted:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Bookmark '{bookmark_tag}' encontrado, mas sem conteudo textual.",
            )
        return extracted

    def first(self) -> str | None:
        return self._extract_optional(1)

    def last(self) -> str | None:
        return self._extract_optional(2)

    def _parse_tipo(self, tipo_finalizacao: int) -> int:
        try:
            tipo = int(tipo_finalizacao)
        except (TypeError, ValueError):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="tipo_finalizacao invalido. Use 1 (livro) ou 2 (traslado).",
            )

        if tipo not in self._BOOKMARK_BY_TIPO:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="tipo_finalizacao invalido. Use 1 (livro) ou 2 (traslado).",
            )
        return tipo

    def _extract_optional(self, tipo_finalizacao: int) -> str | None:
        pattern = self._BOOKMARK_PATTERNS[tipo_finalizacao]
        match = pattern.search(self.content or "")
        if not match:
            return None
        return self._clean_rtf(match.group(1))

    def _clean_rtf(self, text: str) -> str:
        # Quebras de linha e tabulacao semanticas.
        cleaned = re.sub(r"\\par[d]? ?", "\n", text, flags=re.IGNORECASE)
        cleaned = re.sub(r"\\line ?", "\n", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\\tab ?", "\t", cleaned, flags=re.IGNORECASE)

        # Unicode RTF: \u8226? / \u-1234?
        def unicode_repl(match: re.Match[str]) -> str:
            value = int(match.group(1))
            if value < 0:
                value += 65536
            try:
                return chr(value)
            except ValueError:
                return ""

        cleaned = re.sub(r"\\u(-?\d+)\??", unicode_repl, cleaned)

        # Hex escapes RTF: \'e9
        cleaned = re.sub(
            r"\\'([0-9a-fA-F]{2})",
            lambda m: bytes.fromhex(m.group(1)).decode("cp1252", errors="ignore"),
            cleaned,
        )

        # Remove comandos/destinos RTF remanescentes.
        cleaned = re.sub(r"\{\\\*[^{}]*\}", " ", cleaned)
        cleaned = re.sub(r"\\[a-zA-Z]+-?\d* ?", " ", cleaned)
        cleaned = re.sub(r"\\[{}\\]", "", cleaned)
        cleaned = re.sub(r"[{}]", "", cleaned)

        # Normaliza espacos e linhas.
        cleaned = re.sub(r"[ \t]+", " ", cleaned)
        cleaned = re.sub(r"\n\s*\n+", "\n", cleaned)
        return cleaned.strip()
