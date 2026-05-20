from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_banco import get_p_banco_model
from packages.v1.administrativo.schemas.p_banco_schema import (
    PBancoSaveSchema,
    normalize_sim_nao_from_db,
)

_SELECT_COLUMNS = """
    BANCO_ID,
    CODIGO_BANCO,
    DESCRICAO,
    PESSOA_ID,
    LAYOUT_ID,
    APONTAMENTO_PAG_POSTERIOR,
    CUSTAS_NA_CONFIRMACAO,
    DEMAIS_DESPESAS
"""


class SaveRepository(BaseRepository):
    def execute(self, banco_schema: PBancoSaveSchema):
        if use_orm_firebird():
            return self._execute_orm(banco_schema)
        return self._execute_sql(banco_schema)

    def _execute_orm(self, banco_schema: PBancoSaveSchema) -> dict[str, Any]:
        payload = {
            "BANCO_ID": banco_schema.banco_id,
            "CODIGO_BANCO": banco_schema.codigo_banco,
            "DESCRICAO": banco_schema.descricao,
            "LAYOUT_ID": banco_schema.layout_id,
            "APONTAMENTO_PAG_POSTERIOR": banco_schema.apontamento_pag_posterior,
            "CUSTAS_NA_CONFIRMACAO": banco_schema.custas_na_confirmacao,
            "DEMAIS_DESPESAS": None,
        }
        created = get_p_banco_model().create(payload)
        return self._map_banco_row(created) or {}

    def _execute_sql(self, banco_schema: PBancoSaveSchema) -> dict[str, Any]:
        try:
            sql = f"""
            INSERT INTO P_BANCO (
                BANCO_ID,
                CODIGO_BANCO,
                DESCRICAO,
                LAYOUT_ID,
                APONTAMENTO_PAG_POSTERIOR,
                CUSTAS_NA_CONFIRMACAO,
                DEMAIS_DESPESAS
            ) VALUES (
                :banco_id,
                :codigo_banco,
                :descricao,
                :layout_id,
                :apontamento_pag_posterior,
                :custas_na_confirmacao,
                NULL
            )
            RETURNING
                {_SELECT_COLUMNS.strip()};
            """
            params = {
                "banco_id": banco_schema.banco_id,
                "codigo_banco": banco_schema.codigo_banco,
                "descricao": banco_schema.descricao,
                "layout_id": banco_schema.layout_id,
                "apontamento_pag_posterior": banco_schema.apontamento_pag_posterior,
                "custas_na_confirmacao": banco_schema.custas_na_confirmacao,
            }
            result = self.run_and_return(sql, params)
            return self._map_banco_row(result) or {}
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar banco: {exc}",
            ) from exc

    @staticmethod
    def _map_banco_row(row: Optional[Mapping[str, Any]]) -> Optional[dict[str, Any]]:
        mapped = normalize_row_keys(row)
        if mapped is None:
            return None

        for key in ("banco_id", "pessoa_id", "layout_id"):
            value = mapped.get(key)
            if isinstance(value, Decimal):
                mapped[key] = int(value)

        demais = mapped.get("demais_despesas")
        if isinstance(demais, Decimal):
            mapped["demais_despesas"] = float(demais) if demais is not None else None
        mapped["demais_despesas"] = None

        mapped["apontamento_pag_posterior"] = normalize_sim_nao_from_db(
            mapped.get("apontamento_pag_posterior")
        )
        mapped["custas_na_confirmacao"] = normalize_sim_nao_from_db(
            mapped.get("custas_na_confirmacao")
        )

        codigo = mapped.get("codigo_banco")
        if codigo is not None:
            mapped["codigo_banco"] = str(codigo).strip() or None

        return mapped
