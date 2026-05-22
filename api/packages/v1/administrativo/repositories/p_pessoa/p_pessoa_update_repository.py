from __future__ import annotations

from typing import Any

from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from database.orm_firebird_settings import use_orm_firebird
from packages.v1.administrativo.model.p_pessoa import get_p_pessoa_model
from packages.v1.administrativo.schemas.p_pessoa_schema import (
    PPessoaUpdateSchema,
    map_pessoa_row,
    sim_nao_to_db,
)

_RETURNING_COLUMNS = """
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


class UpdateRepository(BaseRepository):
    def execute(self, pessoa_id: int, pessoa_schema: PPessoaUpdateSchema) -> dict[str, Any]:
        if use_orm_firebird():
            return self._execute_orm(pessoa_id, pessoa_schema)
        return self._execute_sql(pessoa_id, pessoa_schema)

    def _execute_orm(
        self, pessoa_id: int, pessoa_schema: PPessoaUpdateSchema
    ) -> dict[str, Any]:
        values = self._build_values(pessoa_schema)
        if not values:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Nenhum campo informado para atualização.",
            )

        model = get_p_pessoa_model()
        result = model.update(values, {"where": {"PESSOA_ID": pessoa_id}})
        rows = result.get("rows") if isinstance(result, dict) else None
        if rows:
            return map_pessoa_row(rows[0]) or {}

        return map_pessoa_row(model.findByPk(pessoa_id)) or {}

    def _execute_sql(
        self, pessoa_id: int, pessoa_schema: PPessoaUpdateSchema
    ) -> dict[str, Any]:
        try:
            updates, params = self._build_sql_updates(pessoa_id, pessoa_schema)
            if not updates:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail="Nenhum campo informado para atualização.",
                )

            sql = f"""
            UPDATE P_PESSOA
            SET {', '.join(updates)}
            WHERE PESSOA_ID = :pessoa_id
            RETURNING
                {_RETURNING_COLUMNS.strip()};
            """
            result = self.run_and_return(sql, params)

            if not result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Pessoa não encontrada para atualização.",
                )

            return map_pessoa_row(result) or {}
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar pessoa: {exc}",
            ) from exc

    @staticmethod
    def _build_values(pessoa_schema: PPessoaUpdateSchema) -> dict[str, Any]:
        values: dict[str, Any] = {}
        data = pessoa_schema.model_dump(exclude_unset=True)

        field_map = {
            "nome": "NOME",
            "cpfcnpj": "CPFCNPJ",
            "endereco": "ENDERECO",
            "bairro": "BAIRRO",
            "cidade": "CIDADE",
            "uf": "UF",
            "cep": "CEP",
            "telefone": "TELEFONE",
            "rg": "RG",
            "observacoes": "OBSERVACOES",
            "banco": "BANCO",
            "agencia": "AGENCIA",
            "conta": "CONTA",
            "nome_banco": "NOME_BANCO",
            "nacionalidade": "NACIONALIDADE",
            "estado_civil_id": "ESTADO_CIVIL_ID",
            "profissao_id": "PROFISSAO_ID",
            "cidade_agencia": "CIDADE_AGENCIA",
            "data_nascimento": "DATA_NASCIMENTO",
            "email": "EMAIL",
            "cidade_id": "CIDADE_ID",
            "data_validade": "DATA_VALIDADE",
            "chave_pessoa_imp": "CHAVE_PESSOA_IMP",
            "cod_cra": "COD_CRA",
            "nome_fantasia": "NOME_FANTASIA",
        }

        for key, column in field_map.items():
            if key in data:
                values[column] = data[key]

        if "micro_empresa" in data:
            values["MICRO_EMPRESA"] = sim_nao_to_db(data["micro_empresa"])

        return values

    def _build_sql_updates(
        self, pessoa_id: int, pessoa_schema: PPessoaUpdateSchema
    ) -> tuple[list[str], dict[str, Any]]:
        values = self._build_values(pessoa_schema)
        updates = [f"{column} = :{column}" for column in values]
        params = dict(values)
        params["pessoa_id"] = pessoa_id
        return updates, params
