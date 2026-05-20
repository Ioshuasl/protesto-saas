from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.g_tb_txmodelogrupo_schema import GTbTxmodelogrupoIdSchema
from packages.v1.administrativo.repositories.g_tb_txmodelogrupo.g_tb_txmodelogrupo_show_repository import ShowRepository


class ShowAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a exibição
    de um registro na tabela G_TB_TXMODELOGRUPO.
    """

    def execute(self, txmodelogrupo_schema: GTbTxmodelogrupoIdSchema):
        """
        Executa a operação de exibição.

        Args:
            txmodelogrupo_schema (GTbTxModeloGrupoIdSchema): O esquema com o ID do registro a ser exibido.

        Returns:
            O resultado da operação de exibição.
        """
        # Instânciamento do repositório
        show_repository = ShowRepository()

        # Execução do repositório
        response = show_repository.execute(txmodelogrupo_schema)

        # Retorno da informação
        return response