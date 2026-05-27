from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.g_sistema import get_g_sistema_model
from packages.v1.administrativo.schemas.g_sistema_schema import GSistemaSaveSchema

SITUACAO_CODIGO_INATIVO = "I"


class SaveRepository(BaseRepository):
    def execute(self, sistema_schema: GSistemaSaveSchema):
        if use_orm_firebird():
            return self._execute_orm(sistema_schema)
        return self._execute_sql(sistema_schema)

    def _execute_orm(self, sistema_schema: GSistemaSaveSchema) -> dict[str, Any]:
        payload = {
            "SISTEMA_ID": sistema_schema.sistema_id,
            "DESCRICAO": sistema_schema.descricao,
            "SITUACAO": sistema_schema.situacao,
            "TIPO_CARTORIO": sistema_schema.tipo_cartorio,
            "VERSAO": sistema_schema.versao,
            "DATA_VERSAO": sistema_schema.data_versao,
            "NOME_EXE": sistema_schema.nome_exe,
        }
        created = get_g_sistema_model().create(payload)
        return self._map_sistema_row(created) or {}

    def _execute_sql(self, sistema_schema: GSistemaSaveSchema) -> dict[str, Any]:
        try:
            sql = """
            INSERT INTO G_SISTEMA (
                SISTEMA_ID,
                DESCRICAO,
                SITUACAO,
                TIPO_CARTORIO,
                VERSAO,
                DATA_VERSAO,
                NOME_EXE
            ) VALUES (
                :sistema_id,
                :descricao,
                :situacao,
                :tipo_cartorio,
                :versao,
                :data_versao,
                :nome_exe
            )
            RETURNING
                SISTEMA_ID,
                DESCRICAO,
                SITUACAO,
                TIPO_CARTORIO,
                VERSAO,
                DATA_VERSAO,
                NOME_EXE;
            """
            params = {
                "sistema_id": sistema_schema.sistema_id,
                "descricao": sistema_schema.descricao,
                "situacao": sistema_schema.situacao,
                "tipo_cartorio": sistema_schema.tipo_cartorio,
                "versao": sistema_schema.versao,
                "data_versao": sistema_schema.data_versao,
                "nome_exe": sistema_schema.nome_exe,
            }
            result = self.run_and_return(sql, params)
            return self._map_sistema_row(result)
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar sistema: {exc}",
            ) from exc

    @staticmethod
    def _map_sistema_row(row: Optional[Mapping[str, Any]]) -> Optional[dict[str, Any]]:
        mapped = normalize_row_keys(row)
        if mapped is None:
            return None

        sistema_id = mapped.get("sistema_id")
        if isinstance(sistema_id, Decimal):
            mapped["sistema_id"] = (
                int(sistema_id) if sistema_id == sistema_id.to_integral_value() else float(sistema_id)
            )

        situacao = mapped.get("situacao")
        if situacao is None or not str(situacao).strip():
            mapped["situacao"] = SITUACAO_CODIGO_INATIVO
        else:
            mapped["situacao"] = str(situacao).strip().upper()

        tipo_cartorio = mapped.get("tipo_cartorio")
        if tipo_cartorio is not None:
            mapped["tipo_cartorio"] = str(tipo_cartorio).strip() or None

        return mapped
