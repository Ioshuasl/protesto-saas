from actions.data.generate_insert_sql import generate_insert_sql
from packages.v1.administrativo.schemas.t_pessoa_schema import TPessoaSaveSchema
from fastapi import HTTPException, status
from abstracts.repository import BaseRepository


class TPessoaSaveRepository(BaseRepository):
    """
    Repositório para a operação de salvamento de um novo registro na tabela g_tb_regimebens.
    """

    def execute(self, t_pessoa_save_schema: TPessoaSaveSchema):
        """
        Executa a operação de salvamento no banco de dados.

        Args:
            regimebens_schema (GTbRegimebensSaveSchema): O esquema com os dados a serem salvos.

        Returns:
            O registro recém-criado.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        try:

            # ----------------------------------------------------
            # Preenchimento dos parâmetros
            # ----------------------------------------------------
            params = t_pessoa_save_schema.model_dump(exclude_unset=True)

            # ----------------------------------------------------
            # Montagem do SQL dinâmico
            # ----------------------------------------------------
            sql = generate_insert_sql("T_PESSOA", params)

            # ----------------------------------------------------
            # Execução do SQL e retorno do registro
            # ----------------------------------------------------
            return self.run_and_return(sql, params)

        except Exception as e:

            # Informa que houve uma falha no salvamento do registro
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar registro: {e}",
            )
