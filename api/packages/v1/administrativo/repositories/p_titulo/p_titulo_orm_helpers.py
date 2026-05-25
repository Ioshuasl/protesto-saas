"""
Helpers ORM de P_TITULO compartilhados por show/save.

O index usa SQL enxuto (p_titulo_index_repository.py); includes de show ficam aqui
para não acoplar show ao index.
"""

from __future__ import annotations

from typing import Any

_PESSOA_VINCULO_INCLUDE: list[dict[str, Any]] = [
    {
        "association": "pessoa",
        "required": False,
        "attributes": ["PESSOA_ID", "NOME", "CPFCNPJ", "MICRO_EMPRESA"],
    },
]

# Sem `andamentos` no título (JOIN ambíguo no Firebird) — carregados em show_repository.
# Sem `pessoa_vinculos` com separate:true (erro vars/__dict__) — attach_pessoa_vinculos.
_TITULO_SHOW_INCLUDES: list[dict[str, Any]] = [
    {
        "association": "ocorrencia",
        "required": False,
        "attributes": ["OCORRENCIAS_ID", "CODIGO", "DESCRICAO", "TIPO"],
    },
    {
        "association": "ocorrencia_andamento",
        "required": False,
        "attributes": ["OCORRENCIA_ANDAMENTO_ID", "CODIGO", "DESCRICAO"],
    },
    {
        "association": "especie",
        "required": False,
        "attributes": ["ESPECIE_ID", "ESPECIE", "DESCRICAO"],
    },
    {
        "association": "banco",
        "required": False,
        "attributes": ["BANCO_ID", "CODIGO_BANCO", "DESCRICAO"],
    },
    {
        "association": "motivo_apontamento",
        "required": False,
        "attributes": ["MOTIVOS_ID", "DESCRICAO"],
    },
    {
        "association": "motivo_cancelamento",
        "required": False,
        "attributes": ["MOTIVOS_CANCELAMENTO_ID", "DESCRICAO"],
    },
]


def attach_pessoa_vinculos(mapped: dict[str, Any], titulo_ids: list[int]) -> None:
    """Carrega vínculos do título em query separada (evita include separate no findOne)."""
    from packages.v1.administrativo.model.p_pessoa_vinculo import get_p_pessoa_vinculo_model
    from packages.v1.administrativo.schemas.p_titulo_schema import _map_pessoa_vinculo_item

    titulo_id = mapped.get("titulo_id")
    if titulo_id is None and titulo_ids:
        titulo_id = titulo_ids[0]
    if titulo_id is not None:
        try:
            titulo_id = int(titulo_id)
        except (TypeError, ValueError):
            titulo_id = None

    if titulo_id is None:
        mapped["pessoa_vinculos"] = []
        return

    rows = get_p_pessoa_vinculo_model().findAll(
        {
            "where": {"TITULO_ID": titulo_id},
            "include": _PESSOA_VINCULO_INCLUDE,
            "order": [("PESSOA_VINCULO_ID", "ASC")],
        }
    )
    mapped["pessoa_vinculos"] = [
        _map_pessoa_vinculo_item(item) for item in (rows or []) if item is not None
    ]
