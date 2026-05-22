from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_andamento import get_p_andamento_model
from packages.v1.administrativo.schemas.p_andamento_schema import (
    PAndamentoSaveSchema,
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


class SaveRepository(BaseRepository):
    def execute(self, andamento_schema: PAndamentoSaveSchema):
        if use_orm_firebird():
            return self._execute_orm(andamento_schema)
        return self._execute_sql(andamento_schema)

    def _execute_orm(self, andamento_schema: PAndamentoSaveSchema) -> dict[str, Any]:
        payload = {
            "ANDAMENTO_ID": andamento_schema.andamento_id,
            "OCORRENCIA_ANDAMENTO_ID": andamento_schema.ocorrencia_andamento_id,
            "DATA_OCORRENCIA": andamento_schema.data_ocorrencia,
            "TITULO_ID": andamento_schema.titulo_id,
            "USUARIO_ID": andamento_schema.usuario_id,
            "ARQUIVO_GERADO": andamento_schema.arquivo_gerado,
            "DATA_GERACAO": andamento_schema.data_geracao,
        }
        created = get_p_andamento_model().create(payload)
        return self._map_andamento_row(created) or {}

    def _execute_sql(self, andamento_schema: PAndamentoSaveSchema) -> dict[str, Any]:
        try:
            sql = f"""
            INSERT INTO P_ANDAMENTO (
                ANDAMENTO_ID,
                OCORRENCIA_ANDAMENTO_ID,
                DATA_OCORRENCIA,
                TITULO_ID,
                USUARIO_ID,
                ARQUIVO_GERADO,
                DATA_GERACAO
            ) VALUES (
                :andamento_id,
                :ocorrencia_andamento_id,
                :data_ocorrencia,
                :titulo_id,
                :usuario_id,
                :arquivo_gerado,
                :data_geracao
            )
            RETURNING
                {_SELECT_COLUMNS.strip()};
            """
            params = {
                "andamento_id": andamento_schema.andamento_id,
                "ocorrencia_andamento_id": andamento_schema.ocorrencia_andamento_id,
                "data_ocorrencia": andamento_schema.data_ocorrencia,
                "titulo_id": andamento_schema.titulo_id,
                "usuario_id": andamento_schema.usuario_id,
                "arquivo_gerado": andamento_schema.arquivo_gerado,
                "data_geracao": andamento_schema.data_geracao,
            }
            result = self.run_and_return(sql, params)
            return self._map_andamento_row(result) or {}
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar andamento: {exc}",
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
