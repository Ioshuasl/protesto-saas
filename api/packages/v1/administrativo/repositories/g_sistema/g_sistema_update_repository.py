from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional, Union

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.g_sistema import get_g_sistema_model
from packages.v1.administrativo.schemas.g_sistema_schema import GSistemaUpdateSchema

SITUACAO_CODIGO_INATIVO = "I"


class UpdateRepository(BaseRepository):
    def execute(
        self,
        sistema_id: Union[int, float],
        sistema_schema: GSistemaUpdateSchema,
    ):
        if use_orm_firebird():
            return self._execute_orm(sistema_id, sistema_schema)
        return self._execute_sql(sistema_id, sistema_schema)

    def _execute_orm(
        self,
        sistema_id: Union[int, float],
        sistema_schema: GSistemaUpdateSchema,
    ) -> dict[str, Any]:
        values: dict[str, Any] = {}

        if sistema_schema.descricao is not None:
            values["DESCRICAO"] = sistema_schema.descricao
        if sistema_schema.situacao is not None:
            values["SITUACAO"] = sistema_schema.situacao
        if sistema_schema.tipo_cartorio is not None:
            values["TIPO_CARTORIO"] = sistema_schema.tipo_cartorio
        if sistema_schema.versao is not None:
            values["VERSAO"] = sistema_schema.versao
        if sistema_schema.data_versao is not None:
            values["DATA_VERSAO"] = sistema_schema.data_versao
        if sistema_schema.nome_exe is not None:
            values["NOME_EXE"] = sistema_schema.nome_exe

        model = get_g_sistema_model()
        result = model.update(values, {"where": {"SISTEMA_ID": sistema_id}})
        rows = result.get("rows") if isinstance(result, dict) else None
        if rows:
            return self._map_sistema_row(rows[0]) or {}

        return self._map_sistema_row(model.findByPk(sistema_id)) or {}

    def _execute_sql(
        self,
        sistema_id: Union[int, float],
        sistema_schema: GSistemaUpdateSchema,
    ) -> dict[str, Any]:
        try:
            updates = []
            params: dict[str, Any] = {"sistema_id": sistema_id}

            if sistema_schema.descricao is not None:
                updates.append("DESCRICAO = :descricao")
                params["descricao"] = sistema_schema.descricao
            if sistema_schema.situacao is not None:
                updates.append("SITUACAO = :situacao")
                params["situacao"] = sistema_schema.situacao
            if sistema_schema.tipo_cartorio is not None:
                updates.append("TIPO_CARTORIO = :tipo_cartorio")
                params["tipo_cartorio"] = sistema_schema.tipo_cartorio
            if sistema_schema.versao is not None:
                updates.append("VERSAO = :versao")
                params["versao"] = sistema_schema.versao
            if sistema_schema.data_versao is not None:
                updates.append("DATA_VERSAO = :data_versao")
                params["data_versao"] = sistema_schema.data_versao
            if sistema_schema.nome_exe is not None:
                updates.append("NOME_EXE = :nome_exe")
                params["nome_exe"] = sistema_schema.nome_exe

            if not updates:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Nenhum campo informado para atualização.",
                )

            sql = f"""
            UPDATE G_SISTEMA
            SET {', '.join(updates)}
            WHERE SISTEMA_ID = :sistema_id
            RETURNING
                SISTEMA_ID,
                DESCRICAO,
                SITUACAO,
                TIPO_CARTORIO,
                VERSAO,
                DATA_VERSAO,
                NOME_EXE;
            """
            result = self.run_and_return(sql, params)

            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Sistema não encontrado para atualização.",
                )

            return self._map_sistema_row(result)
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar sistema: {exc}",
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
