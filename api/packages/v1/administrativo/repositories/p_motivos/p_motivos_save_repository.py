from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_motivos import get_p_motivos_model
from packages.v1.administrativo.schemas.p_motivos_schema import (
    PMotivosSaveSchema,
    situacao_from_db,
    situacao_to_db,
)

_SELECT_COLUMNS = """
    MOTIVOS_ID,
    DESCRICAO,
    SITUACAO,
    CODIGO
"""


class SaveRepository(BaseRepository):
    def execute(self, motivos_schema: PMotivosSaveSchema):
        if use_orm_firebird():
            return self._execute_orm(motivos_schema)
        return self._execute_sql(motivos_schema)

    def _execute_orm(self, motivos_schema: PMotivosSaveSchema) -> dict[str, Any]:
        payload = {
            "MOTIVOS_ID": motivos_schema.motivos_id,
            "DESCRICAO": motivos_schema.descricao,
            "SITUACAO": situacao_to_db(motivos_schema.situacao),
            "CODIGO": motivos_schema.codigo,
        }
        created = get_p_motivos_model().create(payload)
        return self._map_motivos_row(created) or {}

    def _execute_sql(self, motivos_schema: PMotivosSaveSchema) -> dict[str, Any]:
        try:
            sql = f"""
            INSERT INTO P_MOTIVOS (
                MOTIVOS_ID,
                DESCRICAO,
                SITUACAO,
                CODIGO
            ) VALUES (
                :motivos_id,
                :descricao,
                :situacao,
                :codigo
            )
            RETURNING
                {_SELECT_COLUMNS.strip()};
            """
            params = {
                "motivos_id": motivos_schema.motivos_id,
                "descricao": motivos_schema.descricao,
                "situacao": situacao_to_db(motivos_schema.situacao),
                "codigo": motivos_schema.codigo,
            }
            result = self.run_and_return(sql, params)
            return self._map_motivos_row(result) or {}
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar motivo: {exc}",
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
