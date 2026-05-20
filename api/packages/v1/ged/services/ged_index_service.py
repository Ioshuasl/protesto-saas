from fastapi import HTTPException, status

from packages.v1.ged.actions.ged_index_action import GEDIndexAction
from packages.v1.ged.schemas.ged_schema import GEDIndexSchema


class GEDIndexService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de registros na tabela g_tb_regimebens.
    """

    def execute(self, data: GEDIndexSchema):
        """
        Executa a operação de busca de todos os registros no banco de dados.

        Returns:
            A lista de registros encontrados.
        """

        # Executa a busca de todas as ações
        response = GEDIndexAction().execute(data)

        # Verifica se foram localizados registros
        if not response:

            # Retorna uma exceção
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar as pessoas",
            )

        # Retorna as informações localizadas
        return response
