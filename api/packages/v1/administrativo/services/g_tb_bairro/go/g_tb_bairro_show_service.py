from fastapi import HTTPException, status
from packages.v1.administrativo.schemas.g_tb_bairro_schema import GTbBairroIdSchema
from packages.v1.administrativo.actions.g_tb_bairro.g_tb_bairro_show_action import ShowAction

class ShowService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela g_tb_bairro.
    """

    def execute(self, bairro_schema: GTbBairroIdSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            bairro_schema (GTbBairroIdSchema): O esquema com o ID a ser buscado.

        Returns:
            O resultado da busca.
        """
        # Instanciamento da ação
        show_action = ShowAction()

        # Executa a ação em questão
        data = show_action.execute(bairro_schema)

        if not data:
            # Retorna uma exceção
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Não foi possível localizar o registro de Bairro'
            )

        # Retorno da informação
        return data