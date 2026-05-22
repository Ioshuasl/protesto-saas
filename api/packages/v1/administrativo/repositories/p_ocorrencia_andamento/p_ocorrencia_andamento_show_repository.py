from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_ocorrencia_andamento import (
    get_p_ocorrencia_andamento_model,
)
from packages.v1.administrativo.schemas.p_ocorrencia_andamento_schema import (
    POcorrenciaAndamentoIdSchema,
)

_SELECT_COLUMNS = """
    OCORRENCIA_ANDAMENTO_ID,
    CODIGO,
    DESCRICAO
"""


class ShowRepository(BaseRepository):
    def execute(self, ocorrencia_andamento_schema: POcorrenciaAndamentoIdSchema):
        if use_orm_firebird():
            return self._execute_orm(ocorrencia_andamento_schema)
        return self._execute_sql(ocorrencia_andamento_schema)

    def _execute_orm(
        self, ocorrencia_andamento_schema: POcorrenciaAndamentoIdSchema
    ) -> dict[str, Any]:
        row = get_p_ocorrencia_andamento_model().findByPk(
            ocorrencia_andamento_schema.ocorrencia_andamento_id
        )
        result = self._map_row(row)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registro não encontrado",
            )
        return result

    def _execute_sql(
        self, ocorrencia_andamento_schema: POcorrenciaAndamentoIdSchema
    ) -> dict[str, Any]:
        try:
            sql = f"""
            SELECT
                {_SELECT_COLUMNS.strip()}
            FROM P_OCORRENCIA_ANDAMENTO
            WHERE OCORRENCIA_ANDAMENTO_ID = :ocorrencia_andamento_id
            """
            params = {
                "ocorrencia_andamento_id": ocorrencia_andamento_schema.ocorrencia_andamento_id
            }
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
                detail=f"Erro ao buscar ocorrência de andamento: {exc}",
            ) from exc

    @staticmethod
    def _map_row(row: Optional[Mapping[str, Any]]) -> Optional[dict[str, Any]]:
        mapped = normalize_row_keys(row)
        if mapped is None:
            return None

        ocorrencia_andamento_id = mapped.get("ocorrencia_andamento_id")
        if isinstance(ocorrencia_andamento_id, Decimal):
            mapped["ocorrencia_andamento_id"] = int(ocorrencia_andamento_id)

        codigo = mapped.get("codigo")
        if codigo is not None:
            mapped["codigo"] = str(codigo).strip().upper() or None

        descricao = mapped.get("descricao")
        if descricao is not None:
            mapped["descricao"] = str(descricao).strip() or None

        return mapped
