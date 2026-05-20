from fastapi import HTTPException, status
from packages.v1.administrativo.schemas.g_natureza_schema import GNaturezaIdSchema
from packages.v1.administrativo.actions.g_natureza.g_natureza_show_action import ShowAction

class ShowService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela g_natureza.
    """

    def execute(self, natureza_schema: GNaturezaIdSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            natureza_schema (GNaturezaIdSchema): O esquema com o ID a ser buscado.

        Returns:
            O resultado da busca.
        """
        # Instanciamento da ação
        show_action = ShowAction()

        # Executa a ação em questão
        data = show_action.execute(natureza_schema)

        if not data:
            # Retorna uma exceção
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Não foi possível localizar o registro de Natureza'
            )

        # Retorno da informação
        return data