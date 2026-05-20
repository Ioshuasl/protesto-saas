from fastapi import HTTPException, status
from abstracts.repository import BaseRepository
from actions.data.generate_insert_sql import generate_insert_sql
from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoSaveSchema


class TAtoSaveRepository(BaseRepository):
    """
    Repositório responsável pela operação de salvamento de um novo registro
    na tabela T_ATO.
    """

    def execute(self, t_ato_save_schema: TAtoSaveSchema):
        """
        Executa a operação de salvamento no banco de dados.

        Args:
            t_ato_save_schema (TAtoSchema): O esquema com os dados a serem salvos.

        Returns:
            O registro recém-criado.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        try:

            # ----------------------------------------------------
            # Preenchimento dos parâmetros
            # ----------------------------------------------------
            params = t_ato_save_schema.model_dump(exclude_unset=True)
            params["situacao_ato"] = "1"

            # ----------------------------------------------------
            # Montagem do SQL dinâmico
            # ----------------------------------------------------
            sql = generate_insert_sql("T_ATO", params)

            # ----------------------------------------------------
            # Execução do SQL e retorno do registro
            # ----------------------------------------------------
            return self.run_and_return(sql, params)

        except Exception as e:
            # ----------------------------------------------------
            # Tratamento de erros e lançamento de exceção HTTP
            # ----------------------------------------------------
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar registro em T_ATO: {e}",
            )
