from fastapi import HTTPException, status
from packages.v1.administrativo.actions.g_tb_txmodelogrupo.g_tb_txmodelogrupo_index_action import IndexAction


class IndexService:
    """
    Serviço responsável por encapsular a lógica de negócio para a listagem de todos os registros na tabela
    G_TB_TXMODELOGRUPO.
    """

    def execute(self):
        """
        Executa a lógica de negócio para a listagem de todos os registros.

        Returns:
            A lista de todos os registros encontrados.
        """
        # Instanciamento de ação
        index_action = IndexAction()

        # Executa a busca de todas as ações
        data = index_action.execute()

        # Verifica se foi localizado registros
        if not data:
            # Retorna uma exceção
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Não foi possível localizar os grupos de modelo de texto'
            )

        # Retorna as informações localizadas
        return data