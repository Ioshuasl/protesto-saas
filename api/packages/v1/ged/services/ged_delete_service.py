from fastapi import HTTPException, status

from packages.v1.ged.actions.ged_delete_action import GEDDeleteAction
from packages.v1.ged.schemas.ged_schema import GEDIndexSchema


class GEDDeleteService:
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
        # Instanciamento da ação
        t_pessoa_index_action = GEDDeleteAction()

        # Executa a busca de todas as ações
        data = t_pessoa_index_action.execute(data)

        # Verifica se foram localizados registros
        if not data:
            # Retorna uma exceção
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar as pessoas",
            )

        # Retorna as informações localizadas
        return data
