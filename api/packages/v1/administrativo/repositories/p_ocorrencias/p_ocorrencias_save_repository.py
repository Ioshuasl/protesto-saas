from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_ocorrencias import get_p_ocorrencias_model
from packages.v1.administrativo.schemas.p_ocorrencias_schema import (
    POcorrenciasSaveSchema,
    tipo_from_db,
    tipo_to_db,
)

_SELECT_COLUMNS = """
    OCORRENCIAS_ID,
    CODIGO,
    DESCRICAO,
    TIPO
"""


class SaveRepository(BaseRepository):
    def execute(self, ocorrencias_schema: POcorrenciasSaveSchema):
        if use_orm_firebird():
            return self._execute_orm(ocorrencias_schema)
        return self._execute_sql(ocorrencias_schema)

    def _execute_orm(self, ocorrencias_schema: POcorrenciasSaveSchema) -> dict[str, Any]:
        payload = {
            "OCORRENCIAS_ID": ocorrencias_schema.ocorrencias_id,
            "CODIGO": ocorrencias_schema.codigo,
            "DESCRICAO": ocorrencias_schema.descricao,
            "TIPO": tipo_to_db(ocorrencias_schema.tipo),
        }
        created = get_p_ocorrencias_model().create(payload)
        return self._map_ocorrencias_row(created) or {}

    def _execute_sql(self, ocorrencias_schema: POcorrenciasSaveSchema) -> dict[str, Any]:
        try:
            sql = f"""
            INSERT INTO P_OCORRENCIAS (
                OCORRENCIAS_ID,
                CODIGO,
                DESCRICAO,
                TIPO
            ) VALUES (
                :ocorrencias_id,
                :codigo,
                :descricao,
                :tipo
            )
            RETURNING
                {_SELECT_COLUMNS.strip()};
            """
            params = {
                "ocorrencias_id": ocorrencias_schema.ocorrencias_id,
                "codigo": ocorrencias_schema.codigo,
                "descricao": ocorrencias_schema.descricao,
                "tipo": tipo_to_db(ocorrencias_schema.tipo),
            }
            result = self.run_and_return(sql, params)
            return self._map_ocorrencias_row(result) or {}
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar ocorrência: {exc}",
            ) from exc

    @staticmethod
    def _map_ocorrencias_row(
        row: Optional[Mapping[str, Any]],
    ) -> Optional[dict[str, Any]]:
        mapped = normalize_row_keys(row)
        if mapped is None:
            return None

        ocorrencias_id = mapped.get("ocorrencias_id")
        if isinstance(ocorrencias_id, Decimal):
            mapped["ocorrencias_id"] = int(ocorrencias_id)

        codigo = mapped.get("codigo")
        if codigo is not None:
            mapped["codigo"] = str(codigo).strip() or None

        descricao = mapped.get("descricao")
        if descricao is not None:
            mapped["descricao"] = str(descricao).strip() or None

        mapped["tipo"] = tipo_from_db(mapped.get("tipo"))
        return mapped
