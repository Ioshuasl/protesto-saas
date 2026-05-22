from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_ocorrencias import get_p_ocorrencias_model
from packages.v1.administrativo.schemas.p_ocorrencias_schema import (
    POcorrenciasUpdateSchema,
    tipo_from_db,
    tipo_to_db,
)

_SELECT_COLUMNS = """
    OCORRENCIAS_ID,
    CODIGO,
    DESCRICAO,
    TIPO
"""


class UpdateRepository(BaseRepository):
    def execute(self, ocorrencias_id: int, ocorrencias_schema: POcorrenciasUpdateSchema):
        if use_orm_firebird():
            return self._execute_orm(ocorrencias_id, ocorrencias_schema)
        return self._execute_sql(ocorrencias_id, ocorrencias_schema)

    def _execute_orm(
        self, ocorrencias_id: int, ocorrencias_schema: POcorrenciasUpdateSchema
    ) -> dict[str, Any]:
        values: dict[str, Any] = {}

        if ocorrencias_schema.descricao is not None:
            values["DESCRICAO"] = ocorrencias_schema.descricao
        if ocorrencias_schema.codigo is not None:
            values["CODIGO"] = ocorrencias_schema.codigo
        if "tipo" in ocorrencias_schema.model_fields_set:
            values["TIPO"] = tipo_to_db(ocorrencias_schema.tipo)

        model = get_p_ocorrencias_model()
        result = model.update(values, {"where": {"OCORRENCIAS_ID": ocorrencias_id}})
        rows = result.get("rows") if isinstance(result, dict) else None
        if rows:
            return self._map_ocorrencias_row(rows[0]) or {}

        return self._map_ocorrencias_row(model.findByPk(ocorrencias_id)) or {}

    def _execute_sql(
        self, ocorrencias_id: int, ocorrencias_schema: POcorrenciasUpdateSchema
    ) -> dict[str, Any]:
        try:
            updates = []
            params: dict[str, Any] = {"ocorrencias_id": ocorrencias_id}

            if ocorrencias_schema.descricao is not None:
                updates.append("DESCRICAO = :descricao")
                params["descricao"] = ocorrencias_schema.descricao
            if ocorrencias_schema.codigo is not None:
                updates.append("CODIGO = :codigo")
                params["codigo"] = ocorrencias_schema.codigo
            if "tipo" in ocorrencias_schema.model_fields_set:
                db_tipo = tipo_to_db(ocorrencias_schema.tipo)
                if db_tipo is None:
                    updates.append("TIPO = NULL")
                else:
                    updates.append("TIPO = :tipo")
                    params["tipo"] = db_tipo

            if not updates:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Nenhum campo informado para atualização.",
                )

            sql = f"""
            UPDATE P_OCORRENCIAS
            SET {', '.join(updates)}
            WHERE OCORRENCIAS_ID = :ocorrencias_id
            RETURNING
                {_SELECT_COLUMNS.strip()};
            """
            result = self.run_and_return(sql, params)

            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Ocorrência não encontrada para atualização.",
                )

            return self._map_ocorrencias_row(result) or {}
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar ocorrência: {exc}",
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
