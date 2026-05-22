from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_ocorrencias import get_p_ocorrencias_model
from packages.v1.administrativo.schemas.p_ocorrencias_schema import (
    POcorrenciasIdSchema,
    tipo_from_db,
)

_SELECT_COLUMNS = """
    OCORRENCIAS_ID,
    CODIGO,
    DESCRICAO,
    TIPO
"""


class ShowRepository(BaseRepository):
    def execute(self, ocorrencias_schema: POcorrenciasIdSchema):
        if use_orm_firebird():
            return self._execute_orm(ocorrencias_schema)
        return self._execute_sql(ocorrencias_schema)

    def _execute_orm(self, ocorrencias_schema: POcorrenciasIdSchema) -> dict[str, Any]:
        row = get_p_ocorrencias_model().findByPk(ocorrencias_schema.ocorrencias_id)
        result = self._map_ocorrencias_row(row)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registro não encontrado",
            )
        return result

    def _execute_sql(self, ocorrencias_schema: POcorrenciasIdSchema) -> dict[str, Any]:
        try:
            sql = f"""
            SELECT
                {_SELECT_COLUMNS.strip()}
            FROM P_OCORRENCIAS
            WHERE OCORRENCIAS_ID = :ocorrencias_id
            """
            params = {"ocorrencias_id": ocorrencias_schema.ocorrencias_id}
            result = self.fetch_one(sql, params)

            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Registro não encontrado",
                )

            return self._map_ocorrencias_row(result)
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao buscar ocorrência: {exc}",
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
