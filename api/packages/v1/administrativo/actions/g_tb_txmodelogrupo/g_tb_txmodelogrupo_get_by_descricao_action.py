from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.g_tb_txmodelogrupo_schema import GTbTxmodelogrupoDescricaoSchema # Assumindo que um schema similar será criado
from packages.v1.administrativo.repositories.g_tb_txmodelogrupo.g_tb_txmodelogrupo_get_by_descricao_repository import GetByDescricaoRepository # Assumindo que um repositório similar será criado


class GetByDescricaoAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela G_TB_TXMODELOGRUPO por descrição.
    """

    def execute(self, txmodelogrupo_schema: GTbTxmodelogrupoDescricaoSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            txmodelogrupo_schema (GTbTxmodelogrupoDescricaoSchema): O esquema com a descrição a ser buscada.

        Returns:
            O registro encontrado ou None.
        """
        # Instanciamento do repositório
        get_by_descricao_repository = GetByDescricaoRepository()

        # Execução do repositório
        response = get_by_descricao_repository.execute(txmodelogrupo_schema)

        # Retorno da informação
        return response