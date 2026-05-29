from __future__ import annotations

from typing import Any

_ARQUIVO_TITULO_TITULOS_INCLUDE: list[dict[str, Any]] = [
    {
        "association": "titulos",
        "required": False,
        "separate": True,
        "attributes": ["NUMERO_APONTAMENTO"],
        "order": [("TITULO_ID", "ASC")],
    }
]
