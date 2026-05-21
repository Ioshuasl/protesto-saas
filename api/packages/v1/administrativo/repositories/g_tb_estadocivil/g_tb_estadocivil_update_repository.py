from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.g_tb_estadocivil import get_g_tb_estadocivil_model
from packages.v1.administrativo.schemas.g_tb_estadocivil_schema import GTbEstadoCivilUpdateSchema

SITUACAO_CODIGO_INATIVO = "I"

_SELECT_COLUMNS = """
    TB_ESTADOCIVIL_ID,
    DESCRICAO,
    SITUACAO,
    SISTEMA_ID,
    TIPO
"""


class UpdateRepository(BaseRepository):
    def execute(self, tb_estadocivil_id: int, estado_civil_schema: GTbEstadoCivilUpdateSchema):
        if use_orm_firebird():
            return self._execute_orm(tb_estadocivil_id, estado_civil_schema)
        return self._execute_sql(tb_estadocivil_id, estado_civil_schema)

    def _execute_orm(
        self, tb_estadocivil_id: int, estado_civil_schema: GTbEstadoCivilUpdateSchema
    ) -> dict[str, Any] | bool:
        values: dict[str, Any] = {}

        if estado_civil_schema.descricao is not None:
            values["DESCRICAO"] = estado_civil_schema.descricao
        if estado_civil_schema.situacao is not None:
            values["SITUACAO"] = estado_civil_schema.situacao
        if estado_civil_schema.sistema_id is not None:
            values["SISTEMA_ID"] = estado_civil_schema.sistema_id
        if estado_civil_schema.tipo is not None:
            values["TIPO"] = estado_civil_schema.tipo

        if not values:
            return False

        model = get_g_tb_estadocivil_model()
        result = model.update(
            values, {"where": {"TB_ESTADOCIVIL_ID": tb_estadocivil_id}}
        )
        rows = result.get("rows") if isinstance(result, dict) else None
        if rows:
            return self._map_row(rows[0]) or {}

        mapped = self._map_row(model.findByPk(tb_estadocivil_id))
        if not mapped:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Nenhum Estado Civil localizado para esta solicitação",
            )
        return mapped

    def _execute_sql(
        self, tb_estadocivil_id: int, estado_civil_schema: GTbEstadoCivilUpdateSchema
    ) -> dict[str, Any] | bool:
        try:
            updates = []
            params: dict[str, Any] = {}

            if estado_civil_schema.descricao is not None:
                updates.append("DESCRICAO = :descricao")
                params["descricao"] = estado_civil_schema.descricao
            if estado_civil_schema.situacao is not None:
                updates.append("SITUACAO = :situacao")
                params["situacao"] = estado_civil_schema.situacao
            if estado_civil_schema.sistema_id is not None:
                updates.append("SISTEMA_ID = :sistema_id")
                params["sistema_id"] = estado_civil_schema.sistema_id
            if estado_civil_schema.tipo is not None:
                updates.append("TIPO = :tipo")
                params["tipo"] = estado_civil_schema.tipo

            if not updates:
                return False

            params["tb_estadocivil_id"] = tb_estadocivil_id
            sql = f"""
            UPDATE G_TB_ESTADOCIVIL
            SET {', '.join(updates)}
            WHERE TB_ESTADOCIVIL_ID = :tb_estadocivil_id
            RETURNING
                {_SELECT_COLUMNS.strip()};
            """
            result = self.run_and_return(sql, params)

            if not result:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Nenhum Estado Civil localizado para esta solicitação",
                )

            return self._map_row(result) or {}
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar o Estado Civil: {exc}",
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
