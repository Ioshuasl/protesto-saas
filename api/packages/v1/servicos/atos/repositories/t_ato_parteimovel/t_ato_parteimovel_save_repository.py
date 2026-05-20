from fastapi import HTTPException, status
from abstracts.repository import BaseRepository
from actions.data.generate_insert_sql import generate_insert_sql
from packages.v1.servicos.atos.schemas.t_ato_parteimovel_schema import (
    TAtoParteImovelSaveSchema,
)


class TAtoParteImovelSaveRepository(BaseRepository):
    """
    Repositório responsável pela operação de salvamento de um novo registro
    na tabela T_ATO_PARTEIMOVEL.
    """

    def execute(self, t_ato_parteimovel_save_schema: TAtoParteImovelSaveSchema):
        """
        Executa a operação de salvamento no banco de dados.

        Args:
            t_ato_parteimovel_save_schema (TAtoParteImovelSchema): O esquema com os dados a serem salvos.

        Returns:
            O registro recém-criado.

        Raises:
            HTTPException: Caso ocorra um erro na execução da query.
        """
        try:

            # ----------------------------------------------------
            # Preenchimento dos parâmetros
            # ----------------------------------------------------
            params = t_ato_parteimovel_save_schema.model_dump(exclude_unset=True)
            params.pop("usuario_id", None)

            # ----------------------------------------------------
            # Montagem do SQL dinâmico
            # ----------------------------------------------------
            sql = generate_insert_sql("T_ATO_PARTEIMOVEL", params)

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
                detail=f"Erro ao salvar registro em T_ATO_PARTEIMOVEL: {e}",
            )
