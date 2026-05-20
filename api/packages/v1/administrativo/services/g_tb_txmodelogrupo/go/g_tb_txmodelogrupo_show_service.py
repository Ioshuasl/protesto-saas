from fastapi import HTTPException, status
from packages.v1.administrativo.schemas.g_tb_txmodelogrupo_schema import GTbTxmodelogrupoIdSchema # Assumindo que este schema será criado
from packages.v1.administrativo.actions.g_tb_txmodelogrupo.g_tb_txmodelogrupo_show_action import ShowAction # Assumindo que esta action será criada

class ShowService:

    def execute(self, txmodelogrupo_schema: GTbTxmodelogrupoIdSchema):
        """
        Executa a lógica de negócio para a exibição de um registro na tabela
        G_TB_TXMODELOGRUPO pelo ID.
        """
        # Instanciamento de ação
        show_action = ShowAction()

        # Executa a ação em questão
        data = show_action.execute(txmodelogrupo_schema)

        if not data:
            # Retorna uma exceção se o registro não for encontrado
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Não foi possível localizar o registro do grupo de modelo de texto.'
            )

        # Retorno da informação
        return data