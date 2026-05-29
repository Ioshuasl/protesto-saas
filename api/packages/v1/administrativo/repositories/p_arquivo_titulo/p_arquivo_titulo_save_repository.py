from __future__ import annotations

from datetime import datetime
from typing import Any

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_arquivo_titulo import get_p_arquivo_titulo_model
from packages.v1.administrativo.repositories.p_arquivo_titulo.p_arquivo_titulo_index_repository import (
    _SELECT_COLUMNS,
)
from packages.v1.administrativo.schemas.p_arquivo_titulo_schema import (
    PArquivoTituloSaveSchema,
    api_money_to_db,
    map_arquivo_titulo_row,
)

_FIELD_TO_COLUMN = {
    "arquivo_titulo_id": "ARQUIVO_TITULO_ID",
    "data_importacao": "DATA_IMPORTACAO",
    "quantidade": "QUANTIDADE",
    "data_movimento": "DATA_MOVIMENTO",
    "numero_sequencial": "NUMERO_SEQUENCIAL",
    "qtde_registros": "QTDE_REGISTROS",
    "qtde_titulos": "QTDE_TITULOS",
    "qtde_indicacoes": "QTDE_INDICACOES",
    "qtde_originais": "QTDE_ORIGINAIS",
    "soma_vlr_remessa": "SOMA_VLR_REMESSA",
    "soma_qtde_remessa": "SOMA_QTDE_REMESSA",
    "agencia_centralizadora": "AGENCIA_CENTRALIZADORA",
    "codigo_praca": "CODIGO_PRACA",
    "sequencial_header": "SEQUENCIAL_HEADER",
    "nome_arquivo": "NOME_ARQUIVO",
    "portador_nome": "PORTADOR_NOME",
    "complemento_header": "COMPLEMENTO_HEADER",
    "identificacao_registro": "IDENTIFICACAO_REGISTRO",
    "portador_codigo": "PORTADOR_CODIGO",
    "id_transacao_remetente": "ID_TRANSACAO_REMETENTE",
    "id_transacao_destinatario": "ID_TRANSACAO_DESTINATARIO",
    "id_transacao_tipo": "ID_TRANSACAO_TIPO",
    "versao_layout": "VERSAO_LAYOUT",
    "sequencial_footer": "SEQUENCIAL_FOOTER",
    "complemento_registro": "COMPLEMENTO_REGISTRO",
}


class SaveRepository(BaseRepository):
    def execute(self, arquivo_schema: PArquivoTituloSaveSchema) -> dict[str, Any]:
        if use_orm_firebird():
            return self._execute_orm(arquivo_schema)
        return self._execute_sql(arquivo_schema)

    def _execute_orm(self, arquivo_schema: PArquivoTituloSaveSchema) -> dict[str, Any]:
        payload = self._build_payload(arquivo_schema)
        created = get_p_arquivo_titulo_model().create(payload)
        return map_arquivo_titulo_row(created) or {}

    def _execute_sql(self, arquivo_schema: PArquivoTituloSaveSchema) -> dict[str, Any]:
        try:
            payload = self._build_payload(arquivo_schema)
            columns = list(payload.keys())
            values = [f":{column.lower()}" for column in columns]
            params = {column.lower(): value for column, value in payload.items()}

            sql = f"""
            INSERT INTO P_ARQUIVO_TITULO (
                {', '.join(columns)}
            ) VALUES (
                {', '.join(values)}
            )
            RETURNING
                {_SELECT_COLUMNS.strip()};
            """
            result = self.run_and_return(sql, params)
            return map_arquivo_titulo_row(result) or {}
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar arquivo de título: {exc}",
            ) from exc

    @classmethod
    def _build_payload(cls, arquivo_schema: PArquivoTituloSaveSchema) -> dict[str, Any]:
        data = arquivo_schema.model_dump(exclude_none=True)
        payload: dict[str, Any] = {}

        for field, column in _FIELD_TO_COLUMN.items():
            if field not in data:
                continue
            value = data[field]
            if field == "soma_vlr_remessa":
                value = api_money_to_db(value)
            payload[column] = value

        if "DATA_IMPORTACAO" not in payload:
            payload["DATA_IMPORTACAO"] = datetime.now()

        return payload
