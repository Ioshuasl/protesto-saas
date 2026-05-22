from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_motivos_cancelamento import (
    get_p_motivos_cancelamento_model,
)
from packages.v1.administrativo.schemas.p_motivos_cancelamento_schema import (
    PMotivosCancelamentoIdSchema,
    situacao_from_db,
)

_SELECT_COLUMNS = """
    MOTIVOS_CANCELAMENTO_ID,
    DESCRICAO,
    SITUACAO
"""


class ShowRepository(BaseRepository):
    def execute(self, motivos_cancelamento_schema: PMotivosCancelamentoIdSchema):
        if use_orm_firebird():
            return self._execute_orm(motivos_cancelamento_schema)
        return self._execute_sql(motivos_cancelamento_schema)

    def _execute_orm(
        self, motivos_cancelamento_schema: PMotivosCancelamentoIdSchema
    ) -> dict[str, Any]:
        row = get_p_motivos_cancelamento_model().findByPk(
            motivos_cancelamento_schema.motivos_cancelamento_id
        )
        result = self._map_row(row)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registro não encontrado",
            )
        return result

    def _execute_sql(
        self, motivos_cancelamento_schema: PMotivosCancelamentoIdSchema
    ) -> dict[str, Any]:
        try:
            sql = f"""
            SELECT
                {_SELECT_COLUMNS.strip()}
            FROM P_MOTIVOS_CANCELAMENTO
            WHERE MOTIVOS_CANCELAMENTO_ID = :motivos_cancelamento_id
            """
            params = {
                "motivos_cancelamento_id": motivos_cancelamento_schema.motivos_cancelamento_id
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
                detail=f"Erro ao buscar motivo de cancelamento: {exc}",
            ) from exc

    @staticmethod
    def _map_row(row: Optional[Mapping[str, Any]]) -> Optional[dict[str, Any]]:
        mapped = normalize_row_keys(row)
        if mapped is None:
            return None

        pk = mapped.get("motivos_cancelamento_id")
        if isinstance(pk, Decimal):
            mapped["motivos_cancelamento_id"] = int(pk)

        descricao = mapped.get("descricao")
        if descricao is not None:
            mapped["descricao"] = str(descricao).strip() or None

        mapped["situacao"] = situacao_from_db(mapped.get("situacao"))
        return mapped
