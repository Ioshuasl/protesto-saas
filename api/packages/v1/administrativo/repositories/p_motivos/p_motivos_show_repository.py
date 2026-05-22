from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_motivos import get_p_motivos_model
from packages.v1.administrativo.schemas.p_motivos_schema import (
    PMotivosIdSchema,
    situacao_from_db,
)

_SELECT_COLUMNS = """
    MOTIVOS_ID,
    DESCRICAO,
    SITUACAO,
    CODIGO
"""


class ShowRepository(BaseRepository):
    def execute(self, motivos_schema: PMotivosIdSchema):
        if use_orm_firebird():
            return self._execute_orm(motivos_schema)
        return self._execute_sql(motivos_schema)

    def _execute_orm(self, motivos_schema: PMotivosIdSchema) -> dict[str, Any]:
        row = get_p_motivos_model().findByPk(motivos_schema.motivos_id)
        result = self._map_motivos_row(row)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registro não encontrado",
            )
        return result

    def _execute_sql(self, motivos_schema: PMotivosIdSchema) -> dict[str, Any]:
        try:
            sql = f"""
            SELECT
                {_SELECT_COLUMNS.strip()}
            FROM P_MOTIVOS
            WHERE MOTIVOS_ID = :motivos_id
            """
            params = {"motivos_id": motivos_schema.motivos_id}
            result = self.fetch_one(sql, params)

            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Registro não encontrado",
                )

            return self._map_motivos_row(result)
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao buscar motivo: {exc}",
            ) from exc

    @staticmethod
    def _map_motivos_row(row: Optional[Mapping[str, Any]]) -> Optional[dict[str, Any]]:
        mapped = normalize_row_keys(row)
        if mapped is None:
            return None

        motivos_id = mapped.get("motivos_id")
        if isinstance(motivos_id, Decimal):
            mapped["motivos_id"] = int(motivos_id)

        codigo = mapped.get("codigo")
        if codigo is not None:
            mapped["codigo"] = str(codigo).strip() or None

        descricao = mapped.get("descricao")
        if descricao is not None:
            mapped["descricao"] = str(descricao).strip() or None

        mapped["situacao"] = situacao_from_db(mapped.get("situacao"))
        return mapped
