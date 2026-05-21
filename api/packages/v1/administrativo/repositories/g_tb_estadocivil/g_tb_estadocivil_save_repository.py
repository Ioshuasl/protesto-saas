from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.g_tb_estadocivil import get_g_tb_estadocivil_model
from packages.v1.administrativo.schemas.g_tb_estadocivil_schema import GTbEstadoCivilSaveSchema

SITUACAO_CODIGO_INATIVO = "I"


class SaveRepository(BaseRepository):
    def execute(self, estado_civil_schema: GTbEstadoCivilSaveSchema):
        if use_orm_firebird():
            return self._execute_orm(estado_civil_schema)
        return self._execute_sql(estado_civil_schema)

    def _execute_orm(self, estado_civil_schema: GTbEstadoCivilSaveSchema) -> dict[str, Any]:
        payload = {
            "TB_ESTADOCIVIL_ID": estado_civil_schema.tb_estadocivil_id,
            "DESCRICAO": estado_civil_schema.descricao,
            "SITUACAO": estado_civil_schema.situacao,
            "SISTEMA_ID": estado_civil_schema.sistema_id,
            "TIPO": estado_civil_schema.tipo,
        }
        created = get_g_tb_estadocivil_model().create(payload)
        return self._map_row(created) or {}

    def _execute_sql(self, estado_civil_schema: GTbEstadoCivilSaveSchema) -> dict[str, Any]:
        try:
            sql = """
            INSERT INTO G_TB_ESTADOCIVIL (
                TB_ESTADOCIVIL_ID,
                DESCRICAO,
                SITUACAO,
                SISTEMA_ID,
                TIPO
            ) VALUES (
                :tb_estadocivil_id,
                :descricao,
                :situacao,
                :sistema_id,
                :tipo
            )
            RETURNING
                TB_ESTADOCIVIL_ID,
                DESCRICAO,
                SITUACAO,
                SISTEMA_ID,
                TIPO;
            """
            params = {
                "tb_estadocivil_id": estado_civil_schema.tb_estadocivil_id,
                "descricao": estado_civil_schema.descricao,
                "situacao": estado_civil_schema.situacao,
                "sistema_id": estado_civil_schema.sistema_id,
                "tipo": estado_civil_schema.tipo,
            }
            result = self.run_and_return(sql, params)
            return self._map_row(result) or {}
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar Estado Civil: {exc}",
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
