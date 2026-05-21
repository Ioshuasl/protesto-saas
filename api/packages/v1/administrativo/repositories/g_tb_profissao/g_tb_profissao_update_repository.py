from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.g_tb_profissao import get_g_tb_profissao_model
from packages.v1.administrativo.schemas.g_tb_profissao_schema import GTbProfissaoUpdateSchema

SITUACAO_CODIGO_INATIVO = "I"

_SELECT_COLUMNS = """
    TB_PROFISSAO_ID,
    DESCRICAO,
    SITUACAO,
    COD_CBO
"""


class UpdateRepository(BaseRepository):
    def execute(self, tb_profissao_id: float, profissao_schema: GTbProfissaoUpdateSchema):
        if use_orm_firebird():
            return self._execute_orm(tb_profissao_id, profissao_schema)
        return self._execute_sql(tb_profissao_id, profissao_schema)

    def _execute_orm(
        self, tb_profissao_id: float, profissao_schema: GTbProfissaoUpdateSchema
    ) -> dict[str, Any] | bool:
        values: dict[str, Any] = {}

        if profissao_schema.descricao is not None:
            values["DESCRICAO"] = profissao_schema.descricao
        if profissao_schema.situacao is not None:
            values["SITUACAO"] = profissao_schema.situacao
        if profissao_schema.cod_cbo is not None:
            values["COD_CBO"] = profissao_schema.cod_cbo

        if not values:
            return False

        pk = int(tb_profissao_id)
        model = get_g_tb_profissao_model()
        result = model.update(values, {"where": {"TB_PROFISSAO_ID": pk}})
        rows = result.get("rows") if isinstance(result, dict) else None
        if rows:
            return self._map_row(rows[0]) or {}

        mapped = self._map_row(model.findByPk(pk))
        if not mapped:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Nenhuma profissão localizada para esta solicitação",
            )
        return mapped

    def _execute_sql(
        self, tb_profissao_id: float, profissao_schema: GTbProfissaoUpdateSchema
    ) -> dict[str, Any] | bool:
        try:
            updates = []
            params: dict[str, Any] = {}

            if profissao_schema.descricao is not None:
                updates.append("DESCRICAO = :descricao")
                params["descricao"] = profissao_schema.descricao
            if profissao_schema.situacao is not None:
                updates.append("SITUACAO = :situacao")
                params["situacao"] = profissao_schema.situacao
            if profissao_schema.cod_cbo is not None:
                updates.append("COD_CBO = :cod_cbo")
                params["cod_cbo"] = profissao_schema.cod_cbo

            if not updates:
                return False

            params["tb_profissao_id"] = int(tb_profissao_id)
            sql = f"""
            UPDATE G_TB_PROFISSAO
            SET {', '.join(updates)}
            WHERE TB_PROFISSAO_ID = :tb_profissao_id
            RETURNING
                {_SELECT_COLUMNS.strip()};
            """
            result = self.run_and_return(sql, params)

            if not result:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Nenhuma profissão localizada para esta solicitação",
                )

            return self._map_row(result) or {}
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar profissão: {exc}",
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
