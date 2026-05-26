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
from packages.v1.administrativo.schemas.p_certidao_schema import PCertidaoSaveSchema

_FIELD_TO_COLUMN = {
    "certidao_id": "CERTIDAO_ID",
    "usuario_id": "USUARIO_ID",
    "data_certidao": "DATA_CERTIDAO",
    "hora_certidao": "HORA_CERTIDAO",
    "tipo_certidao": "TIPO_CERTIDAO",
    "valor_emolumento": "VALOR_EMOLUMENTO",
    "valor_taxa_judiciaria": "VALOR_TAXA_JUDICIARIA",
    "valor_fundesp": "VALOR_FUNDESP",
    "valor_taxa_extra": "VALOR_TAXA_EXTRA",
    "numero_impressao": "NUMERO_IMPRESSAO",
    "cpfcnpj": "CPFCNPJ",
    "nome": "NOME",
    "status": "STATUS",
    "observacao": "OBSERVACAO",
    "valor_taxa_iss": "VALOR_TAXA_ISS",
    "apresentante": "APRESENTANTE",
    "nfse_id": "NFSE_ID",
    "qtd_protestos": "QTD_PROTESTOS",
    "qtd_cancelados": "QTD_CANCELADOS",
    "qtd_sustado": "QTD_SUSTADO",
    "n_remessa": "N_REMESSA",
    "tipo_remessa": "TIPO_REMESSA",
    "protecao_credito_id": "PROTECAO_CREDITO_ID",
}


class SaveRepository(BaseRepository):
    def execute(self, certidao_schema: PCertidaoSaveSchema) -> dict[str, Any]:
        if use_orm_firebird():
            return self._execute_orm(certidao_schema)
        return self._execute_sql(certidao_schema)

    def _execute_orm(self, certidao_schema: PCertidaoSaveSchema) -> dict[str, Any]:
        payload = self._build_payload(certidao_schema)
        created = get_p_certidao_model().create(payload)
        return IndexRepository._map_row(created) or {}

    def _execute_sql(self, certidao_schema: PCertidaoSaveSchema) -> dict[str, Any]:
        try:
            payload = self._build_payload(certidao_schema)
            columns = list(payload.keys())
            values = [f":{column.lower()}" for column in columns]
            params = {column.lower(): value for column, value in payload.items()}

            sql = f"""
            INSERT INTO P_CERTIDAO (
                {', '.join(columns)}
            ) VALUES (
                {', '.join(values)}
            )
            RETURNING
                {_SELECT_COLUMNS.strip()};
            """
            result = self.run_and_return(sql, params)
            return IndexRepository._map_row(result) or {}
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar certidão: {exc}",
            ) from exc

    @staticmethod
    def _build_payload(certidao_schema: PCertidaoSaveSchema) -> dict[str, Any]:
        data = certidao_schema.model_dump(exclude_none=True)
        return {
            column: data[field]
            for field, column in _FIELD_TO_COLUMN.items()
            if field in data
        }
