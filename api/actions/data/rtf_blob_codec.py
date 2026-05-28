from __future__ import annotations

import ast

from actions.data.text import Text
from orm_py.utils import materialize_blob_value


class RTFBlobCodec:
    @staticmethod
    def _materialize_binary_blob(blob_value):
        if blob_value is None:
            return None

        # Some ORM paths may stringify bytes as: "b'...'"
        if isinstance(blob_value, str):
            stripped = blob_value.strip()
            if (stripped.startswith("b'") and stripped.endswith("'")) or (
                stripped.startswith('b"') and stripped.endswith('"')
            ):
                try:
                    parsed = ast.literal_eval(stripped)
                    if isinstance(parsed, (bytes, bytearray)):
                        blob_value = bytes(parsed)
                except Exception:
                    pass

        try:
            return materialize_blob_value(
                blob_value,
                subtype="binary",
                charset="ISO8859_1",
                binary_mode="bytes",
            )
        except Exception:
            return blob_value

    @staticmethod
    def blob_to_rtf_text(blob_value) -> str:
        """
        Normaliza conteúdo de BLOB para RTF string.
        Suporta payload compactado (rtf-zlib) e texto direto.
        """
        if blob_value is None:
            return ""

        materialized_blob = RTFBlobCodec._materialize_binary_blob(blob_value)
        normalized = Text.decompress(materialized_blob)
        if not normalized:
            return ""

        text = str(normalized).strip()
        if text.startswith("{\\rtf"):
            return text

        return text

    @staticmethod
    def rtf_text_to_blob(rtf_text: str) -> bytes:
        """
        Compacta RTF string para persistência em BLOB (rtf-zlib).
        """
        if not rtf_text:
            return b""
        return Text.compress(rtf_text, encoding="iso-8859-1")

