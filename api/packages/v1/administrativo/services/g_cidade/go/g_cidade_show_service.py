from fastapi import HTTPException, status
from packages.v1.administrativo.schemas.g_cidade_schema import GCidadeIdSchema
from packages.v1.administrativo.actions.g_cidade.g_cidade_show_action import ShowAction

class ShowService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela G_CIDADE pelo seu ID (CIDADE_ID).
    """

    def execute(self, g_cidade_schema: GCidadeIdSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            g_cidade_schema (GCidadeIdSchema): O esquema com o ID a ser buscado.

        Returns:
            O resultado da busca (o registro encontrado).
        """
        # Instanciamento da ação
        show_action = ShowAction()

        # Executa a ação em questão
        data = show_action.execute(g_cidade_schema)

        if not data:
            # Retorna uma exceção se o registro não for encontrado
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Não foi possível localizar o registro de CIDADE'
            )

        # Retorno da informação
        return data