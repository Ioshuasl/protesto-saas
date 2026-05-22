from __future__ import annotations

from typing import Any

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_pessoa_vinculo import get_p_pessoa_vinculo_model
from packages.v1.administrativo.schemas.p_pessoa_vinculo_schema import (
    PPessoaVinculoUpdateSchema,
    build_db_payload_from_schema,
    map_pessoa_vinculo_row,
)

_RETURNING_COLUMNS = """
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


class UpdateRepository(BaseRepository):
    def execute(
        self, pessoa_vinculo_id: int, vinculo_schema: PPessoaVinculoUpdateSchema
    ) -> dict[str, Any]:
        if use_orm_firebird():
            return self._execute_orm(pessoa_vinculo_id, vinculo_schema)
        return self._execute_sql(pessoa_vinculo_id, vinculo_schema)

    def _execute_orm(
        self, pessoa_vinculo_id: int, vinculo_schema: PPessoaVinculoUpdateSchema
    ) -> dict[str, Any]:
        payload = vinculo_schema.model_dump(exclude_none=True)
        if not payload:
            row = get_p_pessoa_vinculo_model().findByPk(pessoa_vinculo_id)
            return map_pessoa_vinculo_row(row) or {}

        orm_payload = build_db_payload_from_schema(payload)
        get_p_pessoa_vinculo_model().update(
            orm_payload, {"where": {"PESSOA_VINCULO_ID": pessoa_vinculo_id}}
        )
        row = get_p_pessoa_vinculo_model().findByPk(pessoa_vinculo_id)
        return map_pessoa_vinculo_row(row) or {}

    def _execute_sql(
        self, pessoa_vinculo_id: int, vinculo_schema: PPessoaVinculoUpdateSchema
    ) -> dict[str, Any]:
        payload = vinculo_schema.model_dump(exclude_none=True)
        if not payload:
            sql = f"""
            SELECT {_RETURNING_COLUMNS.strip()}
            FROM P_PESSOA_VINCULO
            WHERE PESSOA_VINCULO_ID = :pessoa_vinculo_id
            """
            row = self.fetch_one(sql, {"pessoa_vinculo_id": pessoa_vinculo_id})
            return map_pessoa_vinculo_row(row) or {}

        db_payload = build_db_payload_from_schema(payload)
        set_parts = []
        params: dict[str, Any] = {"pessoa_vinculo_id": pessoa_vinculo_id}
        for column, value in db_payload.items():
            key = column.lower()
            set_parts.append(f"{column} = :{key}")
            params[key] = value

        try:
            sql = f"""
            UPDATE P_PESSOA_VINCULO
            SET {", ".join(set_parts)}
            WHERE PESSOA_VINCULO_ID = :pessoa_vinculo_id
            RETURNING {_RETURNING_COLUMNS.strip()};
            """
            result = self.run_and_return(sql, params)
            return map_pessoa_vinculo_row(result) or {}
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar vínculo de pessoa: {exc}",
            ) from exc
