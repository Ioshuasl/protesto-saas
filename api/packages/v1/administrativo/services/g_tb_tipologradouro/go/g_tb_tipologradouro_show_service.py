from fastapi import HTTPException, status
from packages.v1.administrativo.schemas.g_tb_tipologradouro_schema import GTbTipoLogradouroIdSchema
from packages.v1.administrativo.actions.g_tb_tipologradouro.g_tb_tipologradouro_show_action import ShowAction

class ShowService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela g_tb_tipologradouro.
    """

    def execute(self, g_tb_tipologradouro_schema: GTbTipoLogradouroIdSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            g_tb_tipologradouro_schema (GTbTipoLogradouroIdSchema): O esquema com o ID a ser buscado.

        Returns:
            O resultado da busca.
        """
        # Instanciamento da ação
        show_action = ShowAction()

        # Executa a ação em questão
        data = show_action.execute(g_tb_tipologradouro_schema)

        if not data:
            # Retorna uma exceção
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Não foi possível localizar o registro de Tipo de Logradouro'
            )

        # Retorno da informação
        return data