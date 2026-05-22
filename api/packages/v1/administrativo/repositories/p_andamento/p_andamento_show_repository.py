from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_andamento import get_p_andamento_model
from packages.v1.administrativo.schemas.p_andamento_schema import (
    PAndamentoIdSchema,
    arquivo_gerado_from_db,
)

_SELECT_COLUMNS = """
    ANDAMENTO_ID,
    OCORRENCIA_ANDAMENTO_ID,
    DATA_OCORRENCIA,
    TITULO_ID,
    USUARIO_ID,
    ARQUIVO_GERADO,
    DATA_GERACAO
"""


class ShowRepository(BaseRepository):
    def execute(self, andamento_schema: PAndamentoIdSchema):
        if use_orm_firebird():
            return self._execute_orm(andamento_schema)
        return self._execute_sql(andamento_schema)

    def _execute_orm(self, andamento_schema: PAndamentoIdSchema) -> dict[str, Any]:
        row = get_p_andamento_model().findByPk(andamento_schema.andamento_id)
        result = self._map_andamento_row(row)
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Registro não encontrado",
            )
        return result

    def _execute_sql(self, andamento_schema: PAndamentoIdSchema) -> dict[str, Any]:
        try:
            sql = f"""
            SELECT
                {_SELECT_COLUMNS.strip()}
            FROM P_ANDAMENTO
            WHERE ANDAMENTO_ID = :andamento_id
            """
            params = {"andamento_id": andamento_schema.andamento_id}
            result = self.fetch_one(sql, params)

            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Registro não encontrado",
                )

            return self._map_andamento_row(result)
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Erro ao buscar andamento: {exc}",
            ) from exc

    @staticmethod
    def _map_andamento_row(row: Optional[Mapping[str, Any]]) -> Optional[dict[str, Any]]:
        mapped = normalize_row_keys(row)
        if mapped is None:
            return None

        for key in (
            "andamento_id",
            "ocorrencia_andamento_id",
            "titulo_id",
            "usuario_id",
        ):
            value = mapped.get(key)
            if isinstance(value, Decimal):
                mapped[key] = int(value)

        arquivo = mapped.get("arquivo_gerado")
        if arquivo is not None:
            mapped["arquivo_gerado"] = arquivo_gerado_from_db(str(arquivo))

        return mapped
