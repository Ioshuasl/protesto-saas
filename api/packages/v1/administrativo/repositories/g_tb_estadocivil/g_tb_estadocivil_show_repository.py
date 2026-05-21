from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.g_tb_estadocivil import get_g_tb_estadocivil_model
from packages.v1.administrativo.schemas.g_tb_estadocivil_schema import GTbEstadoCivilIdSchema

SITUACAO_CODIGO_INATIVO = "I"

_SELECT_COLUMNS = """
    TB_ESTADOCIVIL_ID,
    DESCRICAO,
    SITUACAO,
    SISTEMA_ID,
    TIPO
"""


class ShowRepository(BaseRepository):
    def execute(self, estado_civil_schema: GTbEstadoCivilIdSchema):
        if use_orm_firebird():
            return self._execute_orm(estado_civil_schema)
        return self._execute_sql(estado_civil_schema)

    def _execute_orm(self, estado_civil_schema: GTbEstadoCivilIdSchema) -> dict[str, Any]:
        row = get_g_tb_estadocivil_model().findByPk(estado_civil_schema.tb_estadocivil_id)
        result = self._map_row(row)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registro não encontrado",
            )
        return result

    def _execute_sql(self, estado_civil_schema: GTbEstadoCivilIdSchema) -> dict[str, Any]:
        try:
            sql = f"""
            SELECT
                {_SELECT_COLUMNS.strip()}
            FROM G_TB_ESTADOCIVIL
            WHERE TB_ESTADOCIVIL_ID = :tb_estadocivil_id
            """
            params = {"tb_estadocivil_id": estado_civil_schema.tb_estadocivil_id}
            result = self.fetch_one(sql, params)

            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Registro não encontrado",
                )

            return self._map_row(result)
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao buscar registro: {exc}",
            ) from exc

    @staticmethod
    def _map_row(row: Optional[Mapping[str, Any]]) -> Optional[dict[str, Any]]:
        mapped = normalize_row_keys(row)
        if mapped is None:
            return None

        for key in ("tb_estadocivil_id", "sistema_id", "tipo"):
            value = mapped.get(key)
            if isinstance(value, Decimal):
                mapped[key] = int(value)

        situacao = mapped.get("situacao")
        if situacao is None or not str(situacao).strip():
            mapped["situacao"] = SITUACAO_CODIGO_INATIVO
        else:
            mapped["situacao"] = str(situacao).strip().upper()

        return mapped
