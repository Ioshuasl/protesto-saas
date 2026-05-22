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
    PMotivosCancelamentoUpdateSchema,
    situacao_from_db,
    situacao_to_db,
)

_SELECT_COLUMNS = """
    MOTIVOS_CANCELAMENTO_ID,
    DESCRICAO,
    SITUACAO
"""


class UpdateRepository(BaseRepository):
    def execute(
        self,
        motivos_cancelamento_id: int,
        motivos_cancelamento_schema: PMotivosCancelamentoUpdateSchema,
    ):
        if use_orm_firebird():
            return self._execute_orm(motivos_cancelamento_id, motivos_cancelamento_schema)
        return self._execute_sql(motivos_cancelamento_id, motivos_cancelamento_schema)

    def _execute_orm(
        self,
        motivos_cancelamento_id: int,
        motivos_cancelamento_schema: PMotivosCancelamentoUpdateSchema,
    ) -> dict[str, Any]:
        values: dict[str, Any] = {}

        if motivos_cancelamento_schema.descricao is not None:
            values["DESCRICAO"] = motivos_cancelamento_schema.descricao
        if motivos_cancelamento_schema.situacao is not None:
            values["SITUACAO"] = situacao_to_db(motivos_cancelamento_schema.situacao)

        model = get_p_motivos_cancelamento_model()
        result = model.update(
            values, {"where": {"MOTIVOS_CANCELAMENTO_ID": motivos_cancelamento_id}}
        )
        rows = result.get("rows") if isinstance(result, dict) else None
        if rows:
            return self._map_row(rows[0]) or {}

        return self._map_row(model.findByPk(motivos_cancelamento_id)) or {}

    def _execute_sql(
        self,
        motivos_cancelamento_id: int,
        motivos_cancelamento_schema: PMotivosCancelamentoUpdateSchema,
    ) -> dict[str, Any]:
        try:
            updates = []
            params: dict[str, Any] = {
                "motivos_cancelamento_id": motivos_cancelamento_id
            }

            if motivos_cancelamento_schema.descricao is not None:
                updates.append("DESCRICAO = :descricao")
                params["descricao"] = motivos_cancelamento_schema.descricao
            if motivos_cancelamento_schema.situacao is not None:
                updates.append("SITUACAO = :situacao")
                params["situacao"] = situacao_to_db(motivos_cancelamento_schema.situacao)

            if not updates:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Nenhum campo informado para atualização.",
                )

            sql = f"""
            UPDATE P_MOTIVOS_CANCELAMENTO
            SET {', '.join(updates)}
            WHERE MOTIVOS_CANCELAMENTO_ID = :motivos_cancelamento_id
            RETURNING
                {_SELECT_COLUMNS.strip()};
            """
            result = self.run_and_return(sql, params)

            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Motivo de cancelamento não encontrado para atualização.",
                )

            return self._map_row(result) or {}
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar motivo de cancelamento: {exc}",
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
