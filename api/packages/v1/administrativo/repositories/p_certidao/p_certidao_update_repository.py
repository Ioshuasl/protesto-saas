from __future__ import annotations

from typing import Any

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_certidao import get_p_certidao_model
from packages.v1.administrativo.repositories.p_certidao.p_certidao_index_repository import (
    _SELECT_COLUMNS,
    IndexRepository,
)
from packages.v1.administrativo.repositories.p_certidao.p_certidao_save_repository import (
    _FIELD_TO_COLUMN,
)
from packages.v1.administrativo.schemas.p_certidao_schema import PCertidaoUpdateSchema


class UpdateRepository(BaseRepository):
    def execute(
        self,
        certidao_id: int,
        certidao_schema: PCertidaoUpdateSchema,
    ) -> dict[str, Any]:
        if use_orm_firebird():
            return self._execute_orm(certidao_id, certidao_schema)
        return self._execute_sql(certidao_id, certidao_schema)

    def _execute_orm(
        self,
        certidao_id: int,
        certidao_schema: PCertidaoUpdateSchema,
    ) -> dict[str, Any]:
        values = self._build_payload(certidao_schema)
        if not values:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Nenhum campo informado para atualização.",
            )

        model = get_p_certidao_model()
        result = model.update(values, {"where": {"CERTIDAO_ID": certidao_id}})
        rows = result.get("rows") if isinstance(result, dict) else None
        if rows:
            return IndexRepository._map_row(rows[0]) or {}

        mapped = IndexRepository._map_row(model.findByPk(certidao_id))
        if not mapped:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Certidão não encontrada para atualização.",
            )
        return mapped

    def _execute_sql(
        self,
        certidao_id: int,
        certidao_schema: PCertidaoUpdateSchema,
    ) -> dict[str, Any]:
        try:
            payload = self._build_payload(certidao_schema)
            if not payload:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Nenhum campo informado para atualização.",
                )

            updates = [f"{column} = :{column.lower()}" for column in payload]
            params = {column.lower(): value for column, value in payload.items()}
            params["certidao_id"] = certidao_id

            sql = f"""
            UPDATE P_CERTIDAO
            SET {', '.join(updates)}
            WHERE CERTIDAO_ID = :certidao_id
            RETURNING
                {_SELECT_COLUMNS.strip()};
            """
            result = self.run_and_return(sql, params)

            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Certidão não encontrada para atualização.",
                )

            return IndexRepository._map_row(result) or {}
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar certidão: {exc}",
            ) from exc

    @staticmethod
    def _build_payload(certidao_schema: PCertidaoUpdateSchema) -> dict[str, Any]:
        data = certidao_schema.model_dump(exclude_none=True, exclude={"certidao_id"})
        return {
            column: data[field]
            for field, column in _FIELD_TO_COLUMN.items()
            if field in data and field != "certidao_id"
        }
