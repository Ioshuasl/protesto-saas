# Importação de bibliotecas
from fastapi import HTTPException, status
from actions.data.generate_insert_sql import generate_insert_sql
from packages.v1.administrativo.schemas.c_caixa_item_schema import CaixaItemSchema
from abstracts.repository import BaseRepository


class Save(BaseRepository):

    def execute(self, caixa_item: CaixaItemSchema, connection=None):

        try:

            # ----------------------------------------------------
            # Preenchimento dos parâmetros
            # ----------------------------------------------------
            params = caixa_item.model_dump(exclude_unset=True)

            # ----------------------------------------------------
            # Montagem do SQL dinâmico
            # ----------------------------------------------------
            sql = generate_insert_sql("C_CAIXA_ITEM", params)

            # ----------------------------------------------------
            # Execução do SQL e retorno do registro
            # ----------------------------------------------------
            return self.run_and_return(sql, params, connection=connection)

        except Exception as e:
            # ----------------------------------------------------
            # Tratamento de erros e lançamento de exceção HTTP
            # ----------------------------------------------------
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar registro em T_SERVICO_ITEMPEDIDO: {e}",
            )
