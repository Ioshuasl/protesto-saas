from __future__ import annotations

from typing import Any

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_pessoa_vinculo import get_p_pessoa_vinculo_model
from packages.v1.administrativo.schemas.p_pessoa_vinculo_schema import (
    PPessoaVinculoSaveSchema,
    build_db_payload_from_schema,
    map_pessoa_vinculo_row,
)

_INSERT_COLUMNS = """
    PESSOA_VINCULO_ID,
    NOME,
    CPFCNPJ,
    ENDERECO,
    BAIRRO,
    CIDADE,
    UF,
    CEP,
    TELEFONE,
    RG,
    TITULO_ID,
    TIPO_VINCULO,
    PESSOA_ID,
    BANCO,
    AGENCIA,
    CONTA,
    NOME_BANCO,
    NACIONALIDADE,
    ESTADO_CIVIL_ID,
    PROFISSAO_ID,
    CIDADE_AGENCIA,
    GERAR_SELO,
    DEVEDOR_DATA_ACEITE,
    DEVEDOR_AGENCIA,
    DEVEDOR_NUMERO_AR,
    DEVEDOR_RECEBIDO_POR,
    DEVEDOR_SITUACAO,
    DEVEDOR_TIPO_ACEITE,
    OCORRENCIA_ID,
    CHAVE_IMPORTACAO,
    DEVEDOR_MICROEMPRESA,
    OCORRENCIA_ANDAMENTO_ID,
    CONTROLE_DEVEDOR
"""


class SaveRepository(BaseRepository):
    def execute(self, vinculo_schema: PPessoaVinculoSaveSchema) -> dict[str, Any]:
        if use_orm_firebird():
            return self._execute_orm(vinculo_schema)
        return self._execute_sql(vinculo_schema)

    def _execute_orm(self, vinculo_schema: PPessoaVinculoSaveSchema) -> dict[str, Any]:
        payload = build_db_payload_from_schema(
            vinculo_schema.model_dump(exclude_none=True),
            include_pessoa_vinculo_id=True,
            pessoa_vinculo_id=vinculo_schema.pessoa_vinculo_id,
        )
        created = get_p_pessoa_vinculo_model().create(payload)
        return map_pessoa_vinculo_row(created) or {}

    def _execute_sql(self, vinculo_schema: PPessoaVinculoSaveSchema) -> dict[str, Any]:
        try:
            data = vinculo_schema.model_dump(exclude_none=True)
            db_payload = build_db_payload_from_schema(
                data,
                include_pessoa_vinculo_id=True,
                pessoa_vinculo_id=vinculo_schema.pessoa_vinculo_id,
            )
            columns = list(db_payload.keys())
            placeholders = [f":{col.lower()}" for col in columns]
            params = {col.lower(): db_payload[col] for col in columns}

            sql = f"""
            INSERT INTO P_PESSOA_VINCULO ({", ".join(columns)})
            VALUES ({", ".join(placeholders)})
            RETURNING {_INSERT_COLUMNS.strip()};
            """
            result = self.run_and_return(sql, params)
            return map_pessoa_vinculo_row(result) or {}
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar vínculo de pessoa: {exc}",
            ) from exc
