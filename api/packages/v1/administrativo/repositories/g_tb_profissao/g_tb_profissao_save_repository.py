from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.g_tb_profissao import get_g_tb_profissao_model
from packages.v1.administrativo.schemas.g_tb_profissao_schema import GTbProfissaoSaveSchema

SITUACAO_CODIGO_INATIVO = "I"


class SaveRepository(BaseRepository):
    def execute(self, profissao_schema: GTbProfissaoSaveSchema):
        if use_orm_firebird():
            return self._execute_orm(profissao_schema)
        return self._execute_sql(profissao_schema)

    def _execute_orm(self, profissao_schema: GTbProfissaoSaveSchema) -> dict[str, Any]:
        payload = {
            "TB_PROFISSAO_ID": profissao_schema.tb_profissao_id,
            "DESCRICAO": profissao_schema.descricao,
            "SITUACAO": profissao_schema.situacao,
            "COD_CBO": profissao_schema.cod_cbo,
        }
        created = get_g_tb_profissao_model().create(payload)
        return self._map_row(created) or {}

    def _execute_sql(self, profissao_schema: GTbProfissaoSaveSchema) -> dict[str, Any]:
        try:
            sql = """
            INSERT INTO G_TB_PROFISSAO (
                TB_PROFISSAO_ID,
                DESCRICAO,
                SITUACAO,
                COD_CBO
            ) VALUES (
                :tb_profissao_id,
                :descricao,
                :situacao,
                :cod_cbo
            )
            RETURNING
                TB_PROFISSAO_ID,
                DESCRICAO,
                SITUACAO,
                COD_CBO;
            """
            params = {
                "tb_profissao_id": profissao_schema.tb_profissao_id,
                "descricao": profissao_schema.descricao,
                "situacao": profissao_schema.situacao,
                "cod_cbo": profissao_schema.cod_cbo,
            }
            result = self.run_and_return(sql, params)
            return self._map_row(result) or {}
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar profissão: {exc}",
            ) from exc

    @staticmethod
    def _map_row(row: Optional[Mapping[str, Any]]) -> Optional[dict[str, Any]]:
        mapped = normalize_row_keys(row)
        if mapped is None:
            return None

        tb_profissao_id = mapped.get("tb_profissao_id")
        if isinstance(tb_profissao_id, Decimal):
            mapped["tb_profissao_id"] = int(tb_profissao_id)

        situacao = mapped.get("situacao")
        if situacao is None or not str(situacao).strip():
            mapped["situacao"] = SITUACAO_CODIGO_INATIVO
        else:
            mapped["situacao"] = str(situacao).strip().upper()

        return mapped
