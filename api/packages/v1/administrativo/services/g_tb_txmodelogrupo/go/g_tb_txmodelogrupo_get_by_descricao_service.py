from fastapi import HTTPException, status
from packages.v1.administrativo.schemas.g_tb_txmodelogrupo_schema import GTbTxmodelogrupoDescricaoSchema
from packages.v1.administrativo.actions.g_tb_txmodelogrupo.g_tb_txmodelogrupo_get_by_descricao_action import GetByDescricaoAction

class GetByDescricaoService:
    """
    Serviço responsável por encapsular a lógica de negócio para a exibição de um registro na tabela
    G_TB_TXMODELOGRUPO pela descrição.
    """

    def execute(self, txmodelogrupo_schema: GTbTxmodelogrupoDescricaoSchema, messageValidate: bool):
        """
        Executa a lógica de negócio para a exibição de um registro na tabela G_TB_TXMODELOGRUPO pela descrição.

        Args:
            txmodelogrupo_schema (GTbTxmodelogrupoDescricaoSchema): O esquema com a descrição a ser buscada.
            messageValidate (bool): Indica se a validação de mensagem deve ser realizada.

        Returns:
            dict: O registro encontrado ou None.

        Raises:
            HTTPException: Se o registro não for encontrado e messageValidate for True.
        """
        # Instanciamento de ação
        get_by_descricao_action = GetByDescricaoAction()

        # Executa a ação em questão
        data = get_by_descricao_action.execute(txmodelogrupo_schema)

        if messageValidate:
            if not data:
                # Retorna uma exceção se o registro não for encontrado
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Não foi possível localizar o registro'
                )

        # Retorno da informação
        return data