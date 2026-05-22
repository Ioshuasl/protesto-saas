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
    PMotivosCancelamentoSaveSchema,
    situacao_from_db,
    situacao_to_db,
)

_SELECT_COLUMNS = """
    MOTIVOS_CANCELAMENTO_ID,
    DESCRICAO,
    SITUACAO
"""


class SaveRepository(BaseRepository):
    def execute(self, motivos_cancelamento_schema: PMotivosCancelamentoSaveSchema):
        if use_orm_firebird():
            return self._execute_orm(motivos_cancelamento_schema)
        return self._execute_sql(motivos_cancelamento_schema)

    def _execute_orm(
        self, motivos_cancelamento_schema: PMotivosCancelamentoSaveSchema
    ) -> dict[str, Any]:
        payload = {
            "MOTIVOS_CANCELAMENTO_ID": motivos_cancelamento_schema.motivos_cancelamento_id,
            "DESCRICAO": motivos_cancelamento_schema.descricao,
            "SITUACAO": situacao_to_db(motivos_cancelamento_schema.situacao),
        }
        created = get_p_motivos_cancelamento_model().create(payload)
        return self._map_row(created) or {}

    def _execute_sql(
        self, motivos_cancelamento_schema: PMotivosCancelamentoSaveSchema
    ) -> dict[str, Any]:
        try:
            sql = f"""
            INSERT INTO P_MOTIVOS_CANCELAMENTO (
                MOTIVOS_CANCELAMENTO_ID,
                DESCRICAO,
                SITUACAO
            ) VALUES (
                :motivos_cancelamento_id,
                :descricao,
                :situacao
            )
            RETURNING
                {_SELECT_COLUMNS.strip()};
            """
            params = {
                "motivos_cancelamento_id": motivos_cancelamento_schema.motivos_cancelamento_id,
                "descricao": motivos_cancelamento_schema.descricao,
                "situacao": situacao_to_db(motivos_cancelamento_schema.situacao),
            }
            result = self.run_and_return(sql, params)
            return self._map_row(result) or {}
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar motivo de cancelamento: {exc}",
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
