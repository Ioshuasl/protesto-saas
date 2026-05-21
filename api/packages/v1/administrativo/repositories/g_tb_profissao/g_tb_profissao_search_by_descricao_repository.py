from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.g_tb_profissao import get_g_tb_profissao_model
from packages.v1.administrativo.schemas.g_tb_profissao_schema import GTbProfissaoDescricaoSchema

SITUACAO_CODIGO_INATIVO = "I"

_SELECT_COLUMNS = """
    TB_PROFISSAO_ID,
    DESCRICAO,
    SITUACAO,
    COD_CBO
"""


class SearchByDescricaoRepository(BaseRepository):
    def execute(self, profissao_schema: GTbProfissaoDescricaoSchema):
        if use_orm_firebird():
            return self._execute_orm(profissao_schema)
        return self._execute_sql(profissao_schema)

    def _execute_orm(
        self, profissao_schema: GTbProfissaoDescricaoSchema
    ) -> list[dict[str, Any]]:
        # UPPER(DESCRICAO) LIKE — SQL explícito (mesmo padrão de g_feriado com VARCHAR).
        return self._execute_sql(profissao_schema)

    def _execute_sql(
        self, profissao_schema: GTbProfissaoDescricaoSchema
    ) -> list[dict[str, Any]]:
        sql = f"""
        SELECT
            {_SELECT_COLUMNS.strip()}
        FROM G_TB_PROFISSAO
        WHERE UPPER(DESCRICAO) LIKE :descricao
        ORDER BY DESCRICAO
        """
        params = {
            "descricao": f"%{(profissao_schema.descricao or '').strip().upper()}%",
        }
        rows = self.fetch_all(sql, params)
        return [self._map_row(row) or {} for row in rows]

    @staticmethod
    def _map_row(row: Optional[Mapping[str, Any]]) -> Optional[dict[str, Any]]:
        mapped = normalize_row_keys(row)
        if mapped is None:
            return None

        tb_profissao_id = mapped.get("tb_profissao_id")
        if isinstance(tb_profissao_id, Decimal):
            mapped["tb_profissao_id"] = int(tb_profissao_id)

        situacao = mapped.get("situacao")
        if situacao is None or not str(situacao).strip():
            mapped["situacao"] = SITUACAO_CODIGO_INATIVO
        else:
            mapped["situacao"] = str(situacao).strip().upper()

        return mapped
