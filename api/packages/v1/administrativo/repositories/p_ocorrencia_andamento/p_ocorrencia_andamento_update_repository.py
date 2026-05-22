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
    POcorrenciaAndamentoUpdateSchema,
)

_SELECT_COLUMNS = """
    OCORRENCIA_ANDAMENTO_ID,
    CODIGO,
    DESCRICAO
"""


class UpdateRepository(BaseRepository):
    def execute(
        self,
        ocorrencia_andamento_id: int,
        ocorrencia_andamento_schema: POcorrenciaAndamentoUpdateSchema,
    ):
        if use_orm_firebird():
            return self._execute_orm(ocorrencia_andamento_id, ocorrencia_andamento_schema)
        return self._execute_sql(ocorrencia_andamento_id, ocorrencia_andamento_schema)

    def _execute_orm(
        self,
        ocorrencia_andamento_id: int,
        ocorrencia_andamento_schema: POcorrenciaAndamentoUpdateSchema,
    ) -> dict[str, Any]:
        values: dict[str, Any] = {}

        if ocorrencia_andamento_schema.descricao is not None:
            values["DESCRICAO"] = ocorrencia_andamento_schema.descricao
        if ocorrencia_andamento_schema.codigo is not None:
            values["CODIGO"] = ocorrencia_andamento_schema.codigo

        model = get_p_ocorrencia_andamento_model()
        result = model.update(
            values, {"where": {"OCORRENCIA_ANDAMENTO_ID": ocorrencia_andamento_id}}
        )
        rows = result.get("rows") if isinstance(result, dict) else None
        if rows:
            return self._map_row(rows[0]) or {}

        return self._map_row(model.findByPk(ocorrencia_andamento_id)) or {}

    def _execute_sql(
        self,
        ocorrencia_andamento_id: int,
        ocorrencia_andamento_schema: POcorrenciaAndamentoUpdateSchema,
    ) -> dict[str, Any]:
        try:
            updates = []
            params: dict[str, Any] = {"ocorrencia_andamento_id": ocorrencia_andamento_id}

            if ocorrencia_andamento_schema.descricao is not None:
                updates.append("DESCRICAO = :descricao")
                params["descricao"] = ocorrencia_andamento_schema.descricao
            if ocorrencia_andamento_schema.codigo is not None:
                updates.append("CODIGO = :codigo")
                params["codigo"] = ocorrencia_andamento_schema.codigo

            if not updates:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Nenhum campo informado para atualização.",
                )

            sql = f"""
            UPDATE P_OCORRENCIA_ANDAMENTO
            SET {', '.join(updates)}
            WHERE OCORRENCIA_ANDAMENTO_ID = :ocorrencia_andamento_id
            RETURNING
                {_SELECT_COLUMNS.strip()};
            """
            result = self.run_and_return(sql, params)

            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Ocorrência de andamento não encontrada para atualização.",
                )

            return self._map_row(result) or {}
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar ocorrência de andamento: {exc}",
            ) from exc

    @staticmethod
    def _map_row(row: Optional[Mapping[str, Any]]) -> Optional[dict[str, Any]]:
        mapped = normalize_row_keys(row)
        if mapped is None:
            return None

        pk = mapped.get("ocorrencia_andamento_id")
        if isinstance(pk, Decimal):
            mapped["ocorrencia_andamento_id"] = int(pk)

        codigo = mapped.get("codigo")
        if codigo is not None:
            mapped["codigo"] = str(codigo).strip().upper() or None

        descricao = mapped.get("descricao")
        if descricao is not None:
            mapped["descricao"] = str(descricao).strip() or None

        return mapped
