from __future__ import annotations

from typing import Any

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_pessoa import get_p_pessoa_model
from packages.v1.administrativo.schemas.p_pessoa_schema import (
    PPessoaSaveSchema,
    map_pessoa_row,
    sim_nao_to_db,
)

_SELECT_COLUMNS = """
    PESSOA_ID,
    NOME,
    CPFCNPJ,
    ENDERECO,
    BAIRRO,
    CIDADE,
    UF,
    CEP,
    TELEFONE,
    RG,
    OBSERVACOES,
    BANCO,
    AGENCIA,
    CONTA,
    NOME_BANCO,
    NACIONALIDADE,
    ESTADO_CIVIL_ID,
    PROFISSAO_ID,
    CIDADE_AGENCIA,
    DATA_NASCIMENTO,
    EMAIL,
    CIDADE_ID,
    DATA_VALIDADE,
    MICRO_EMPRESA,
    CHAVE_PESSOA_IMP,
    COD_CRA,
    NOME_FANTASIA
"""


class SaveRepository(BaseRepository):
    def execute(self, pessoa_schema: PPessoaSaveSchema) -> dict[str, Any]:
        if use_orm_firebird():
            return self._execute_orm(pessoa_schema)
        return self._execute_sql(pessoa_schema)

    def _execute_orm(self, pessoa_schema: PPessoaSaveSchema) -> dict[str, Any]:
        created = get_p_pessoa_model().create(self._build_payload(pessoa_schema))
        return map_pessoa_row(created) or {}

    def _execute_sql(self, pessoa_schema: PPessoaSaveSchema) -> dict[str, Any]:
        try:
            payload = self._build_payload(pessoa_schema)
            sql = f"""
            INSERT INTO P_PESSOA (
                PESSOA_ID,
                NOME,
                CPFCNPJ,
                ENDERECO,
                BAIRRO,
                CIDADE,
                UF,
                CEP,
                TELEFONE,
                RG,
                OBSERVACOES,
                BANCO,
                AGENCIA,
                CONTA,
                NOME_BANCO,
                NACIONALIDADE,
                ESTADO_CIVIL_ID,
                PROFISSAO_ID,
                CIDADE_AGENCIA,
                DATA_NASCIMENTO,
                EMAIL,
                CIDADE_ID,
                DATA_VALIDADE,
                MICRO_EMPRESA,
                CHAVE_PESSOA_IMP,
                COD_CRA,
                NOME_FANTASIA
            ) VALUES (
                :PESSOA_ID,
                :NOME,
                :CPFCNPJ,
                :ENDERECO,
                :BAIRRO,
                :CIDADE,
                :UF,
                :CEP,
                :TELEFONE,
                :RG,
                :OBSERVACOES,
                :BANCO,
                :AGENCIA,
                :CONTA,
                :NOME_BANCO,
                :NACIONALIDADE,
                :ESTADO_CIVIL_ID,
                :PROFISSAO_ID,
                :CIDADE_AGENCIA,
                :DATA_NASCIMENTO,
                :EMAIL,
                :CIDADE_ID,
                :DATA_VALIDADE,
                :MICRO_EMPRESA,
                :CHAVE_PESSOA_IMP,
                :COD_CRA,
                :NOME_FANTASIA
            )
            RETURNING
                {_SELECT_COLUMNS.strip()};
            """
            result = self.run_and_return(sql, payload)
            return map_pessoa_row(result) or {}
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar pessoa: {exc}",
            ) from exc

    @staticmethod
    def _build_payload(pessoa_schema: PPessoaSaveSchema) -> dict[str, Any]:
        return {
            "PESSOA_ID": pessoa_schema.pessoa_id,
            "NOME": pessoa_schema.nome,
            "CPFCNPJ": pessoa_schema.cpfcnpj,
            "ENDERECO": pessoa_schema.endereco,
            "BAIRRO": pessoa_schema.bairro,
            "CIDADE": pessoa_schema.cidade,
            "UF": pessoa_schema.uf,
            "CEP": pessoa_schema.cep,
            "TELEFONE": pessoa_schema.telefone,
            "RG": pessoa_schema.rg,
            "OBSERVACOES": pessoa_schema.observacoes,
            "BANCO": pessoa_schema.banco,
            "AGENCIA": pessoa_schema.agencia,
            "CONTA": pessoa_schema.conta,
            "NOME_BANCO": pessoa_schema.nome_banco,
            "NACIONALIDADE": pessoa_schema.nacionalidade,
            "ESTADO_CIVIL_ID": pessoa_schema.estado_civil_id,
            "PROFISSAO_ID": pessoa_schema.profissao_id,
            "CIDADE_AGENCIA": pessoa_schema.cidade_agencia,
            "DATA_NASCIMENTO": pessoa_schema.data_nascimento,
            "EMAIL": pessoa_schema.email,
            "CIDADE_ID": pessoa_schema.cidade_id,
            "DATA_VALIDADE": pessoa_schema.data_validade,
            "MICRO_EMPRESA": sim_nao_to_db(pessoa_schema.micro_empresa),
            "CHAVE_PESSOA_IMP": pessoa_schema.chave_pessoa_imp,
            "COD_CRA": pessoa_schema.cod_cra,
            "NOME_FANTASIA": pessoa_schema.nome_fantasia,
        }
