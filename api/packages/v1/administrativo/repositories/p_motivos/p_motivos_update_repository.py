from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_motivos import get_p_motivos_model
from packages.v1.administrativo.schemas.p_motivos_schema import (
    PMotivosUpdateSchema,
    situacao_from_db,
    situacao_to_db,
)

_SELECT_COLUMNS = """
    MOTIVOS_ID,
    DESCRICAO,
    SITUACAO,
    CODIGO
"""


class UpdateRepository(BaseRepository):
    def execute(self, motivos_id: int, motivos_schema: PMotivosUpdateSchema):
        if use_orm_firebird():
            return self._execute_orm(motivos_id, motivos_schema)
        return self._execute_sql(motivos_id, motivos_schema)

    def _execute_orm(
        self, motivos_id: int, motivos_schema: PMotivosUpdateSchema
    ) -> dict[str, Any]:
        values: dict[str, Any] = {}

        if motivos_schema.descricao is not None:
            values["DESCRICAO"] = motivos_schema.descricao
        if motivos_schema.codigo is not None:
            values["CODIGO"] = motivos_schema.codigo
        if motivos_schema.situacao is not None:
            values["SITUACAO"] = situacao_to_db(motivos_schema.situacao)

        model = get_p_motivos_model()
        result = model.update(values, {"where": {"MOTIVOS_ID": motivos_id}})
        rows = result.get("rows") if isinstance(result, dict) else None
        if rows:
            return self._map_motivos_row(rows[0]) or {}

        return self._map_motivos_row(model.findByPk(motivos_id)) or {}

    def _execute_sql(
        self, motivos_id: int, motivos_schema: PMotivosUpdateSchema
    ) -> dict[str, Any]:
        try:
            updates = []
            params: dict[str, Any] = {"motivos_id": motivos_id}

            if motivos_schema.descricao is not None:
                updates.append("DESCRICAO = :descricao")
                params["descricao"] = motivos_schema.descricao
            if motivos_schema.codigo is not None:
                updates.append("CODIGO = :codigo")
                params["codigo"] = motivos_schema.codigo
            if motivos_schema.situacao is not None:
                updates.append("SITUACAO = :situacao")
                params["situacao"] = situacao_to_db(motivos_schema.situacao)

            if not updates:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Nenhum campo informado para atualização.",
                )

            sql = f"""
            UPDATE P_MOTIVOS
            SET {', '.join(updates)}
            WHERE MOTIVOS_ID = :motivos_id
            RETURNING
                {_SELECT_COLUMNS.strip()};
            """
            result = self.run_and_return(sql, params)

            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Motivo não encontrado para atualização.",
                )

            return self._map_motivos_row(result) or {}
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar motivo: {exc}",
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
