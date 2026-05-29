from __future__ import annotations

import ast
from typing import Any, Optional

from actions.data.text import Text
from orm_py import materialize_blob_value
from orm_py.utils.blob_utils import _coerce_blob_to_bytes


class BinaryBlobCodec:
    """
    Materializa BLOB SUB_TYPE BINARY (Firebird) e decodifica para texto.

    Usa orm_py.materialize_blob_value (subtype=binary) e Text.decompress
    (zlib / rtf-zlib / texto ISO-8859-1).
  """

    @staticmethod
    def materialize(blob_value: Any) -> Any:
        if blob_value is None:
            return None

        coerced = _coerce_blob_to_bytes(blob_value, charset="ISO8859_1")
        if coerced is not None:
            blob_value = coerced

        if isinstance(blob_value, memoryview):
            blob_value = blob_value.tobytes()

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
    def to_text(blob_value: Any) -> Optional[str]:
        """Retorna o conteúdo integral decodificado (sem truncar nem strip)."""
        materialized = BinaryBlobCodec.materialize(blob_value)
        if materialized is None:
            return None

        if isinstance(materialized, (bytes, bytearray, memoryview)):
            text = Text.decompress(materialized)
        else:
            text = str(materialized)

        if text is None or text == "":
            return None
        return text
