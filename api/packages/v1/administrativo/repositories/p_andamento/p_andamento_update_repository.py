from __future__ import annotations

from decimal import Decimal
from typing import Any, Mapping, Optional

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird import normalize_row_keys
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_andamento import get_p_andamento_model
from packages.v1.administrativo.schemas.p_andamento_schema import (
    PAndamentoUpdateSchema,
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


class UpdateRepository(BaseRepository):
    def execute(self, andamento_id: int, andamento_schema: PAndamentoUpdateSchema):
        if use_orm_firebird():
            return self._execute_orm(andamento_id, andamento_schema)
        return self._execute_sql(andamento_id, andamento_schema)

    def _execute_orm(
        self, andamento_id: int, andamento_schema: PAndamentoUpdateSchema
    ) -> dict[str, Any]:
        values: dict[str, Any] = {}

        if andamento_schema.ocorrencia_andamento_id is not None:
            values["OCORRENCIA_ANDAMENTO_ID"] = andamento_schema.ocorrencia_andamento_id
        if andamento_schema.data_ocorrencia is not None:
            values["DATA_OCORRENCIA"] = andamento_schema.data_ocorrencia
        if andamento_schema.titulo_id is not None:
            values["TITULO_ID"] = andamento_schema.titulo_id
        if andamento_schema.usuario_id is not None:
            values["USUARIO_ID"] = andamento_schema.usuario_id
        if andamento_schema.arquivo_gerado is not None:
            values["ARQUIVO_GERADO"] = andamento_schema.arquivo_gerado
        if andamento_schema.data_geracao is not None:
            values["DATA_GERACAO"] = andamento_schema.data_geracao

        model = get_p_andamento_model()
        result = model.update(values, {"where": {"ANDAMENTO_ID": andamento_id}})
        rows = result.get("rows") if isinstance(result, dict) else None
        if rows:
            return self._map_andamento_row(rows[0]) or {}

        return self._map_andamento_row(model.findByPk(andamento_id)) or {}

    def _execute_sql(
        self, andamento_id: int, andamento_schema: PAndamentoUpdateSchema
    ) -> dict[str, Any]:
        try:
            updates = []
            params: dict[str, Any] = {"andamento_id": andamento_id}

            if andamento_schema.ocorrencia_andamento_id is not None:
                updates.append("OCORRENCIA_ANDAMENTO_ID = :ocorrencia_andamento_id")
                params["ocorrencia_andamento_id"] = (
                    andamento_schema.ocorrencia_andamento_id
                )
            if andamento_schema.data_ocorrencia is not None:
                updates.append("DATA_OCORRENCIA = :data_ocorrencia")
                params["data_ocorrencia"] = andamento_schema.data_ocorrencia
            if andamento_schema.titulo_id is not None:
                updates.append("TITULO_ID = :titulo_id")
                params["titulo_id"] = andamento_schema.titulo_id
            if andamento_schema.usuario_id is not None:
                updates.append("USUARIO_ID = :usuario_id")
                params["usuario_id"] = andamento_schema.usuario_id
            if andamento_schema.arquivo_gerado is not None:
                updates.append("ARQUIVO_GERADO = :arquivo_gerado")
                params["arquivo_gerado"] = andamento_schema.arquivo_gerado
            if andamento_schema.data_geracao is not None:
                updates.append("DATA_GERACAO = :data_geracao")
                params["data_geracao"] = andamento_schema.data_geracao

            if not updates:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Nenhum campo informado para atualização.",
                )

            sql = f"""
            UPDATE P_ANDAMENTO
            SET {', '.join(updates)}
            WHERE ANDAMENTO_ID = :andamento_id
            RETURNING
                {_SELECT_COLUMNS.strip()};
            """
            result = self.run_and_return(sql, params)

            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Andamento não encontrado para atualização.",
                )

            return self._map_andamento_row(result) or {}
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar andamento: {exc}",
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
