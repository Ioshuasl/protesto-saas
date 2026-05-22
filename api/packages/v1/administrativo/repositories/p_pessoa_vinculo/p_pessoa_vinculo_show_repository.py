from __future__ import annotations

from typing import Any, Optional

from abstracts.repository import BaseRepository
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_pessoa_vinculo import get_p_pessoa_vinculo_model
from packages.v1.administrativo.schemas.p_pessoa_vinculo_schema import (
    PPessoaVinculoIdSchema,
    map_pessoa_vinculo_row,
)

_SHOW_INCLUDES = [
    {
        "association": "pessoa",
        "required": False,
        "attributes": ["PESSOA_ID", "NOME", "CPFCNPJ"],
    },
    {
        "association": "titulo",
        "required": False,
        "attributes": ["TITULO_ID", "NUMERO_TITULO", "NUMERO_APONTAMENTO"],
    },
]


class ShowRepository(BaseRepository):
    def execute(self, vinculo_schema: PPessoaVinculoIdSchema) -> Optional[dict[str, Any]]:
        if use_orm_firebird():
            return self._execute_orm(vinculo_schema)
        return self._execute_sql(vinculo_schema)

    def _execute_orm(self, vinculo_schema: PPessoaVinculoIdSchema) -> Optional[dict[str, Any]]:
        row = get_p_pessoa_vinculo_model().findOne(
            {
                "where": {"PESSOA_VINCULO_ID": vinculo_schema.pessoa_vinculo_id},
                "include": _SHOW_INCLUDES,
            }
        )
        return map_pessoa_vinculo_row(row)

    def _execute_sql(self, vinculo_schema: PPessoaVinculoIdSchema) -> Optional[dict[str, Any]]:
        sql = """
        SELECT
            pv.*,
            p.PESSOA_ID AS PESSOA_PESSOA_ID,
            p.NOME AS PESSOA_NOME,
            p.CPFCNPJ AS PESSOA_CPFCNPJ,
            t.TITULO_ID AS TITULO_TITULO_ID,
            t.NUMERO_TITULO AS TITULO_NUMERO_TITULO,
            t.NUMERO_APONTAMENTO AS TITULO_NUMERO_APONTAMENTO
        FROM P_PESSOA_VINCULO pv
        LEFT JOIN P_PESSOA p ON p.PESSOA_ID = pv.PESSOA_ID
        LEFT JOIN P_TITULO t ON t.TITULO_ID = pv.TITULO_ID
        WHERE pv.PESSOA_VINCULO_ID = :pessoa_vinculo_id
        """
        row = self.fetch_one(sql, {"pessoa_vinculo_id": vinculo_schema.pessoa_vinculo_id})
        if row is None:
            return None

        mapped = map_pessoa_vinculo_row(row) or {}
        if row.get("PESSOA_PESSOA_ID") is not None:
            mapped["pessoa"] = {
                "pessoa_id": int(row.get("PESSOA_PESSOA_ID")),
                "nome": row.get("PESSOA_NOME"),
                "cpfcnpj": row.get("PESSOA_CPFCNPJ"),
            }
        if row.get("TITULO_TITULO_ID") is not None:
            mapped["titulo"] = {
                "titulo_id": int(row.get("TITULO_TITULO_ID")),
                "numero_titulo": row.get("TITULO_NUMERO_TITULO"),
                "numero_apontamento": row.get("TITULO_NUMERO_APONTAMENTO"),
            }
        return mapped
