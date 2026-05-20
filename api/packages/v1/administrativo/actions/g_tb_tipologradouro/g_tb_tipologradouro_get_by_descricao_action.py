from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.g_tb_tipologradouro_schema import GTbTipoLogradouroDescricaoSchema
from packages.v1.administrativo.repositories.g_tb_tipologradouro.g_tb_tipologradouro_get_by_descricao_repository import GetByDescricaoRepository


class GetByDescricaoAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela g_tb_tipologradouro por descrição.
    """

    def execute(self, tipologradouro_schema: GTbTipoLogradouroDescricaoSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            tipologradouro_schema (GTbTipologradouroDescricaoSchema): O esquema com a descrição a ser buscada.

        Returns:
            O registro encontrado ou None.
        """
        # Instanciamento do repositório
        show_repository = GetByDescricaoRepository()

        # Execução do repositório
        response = show_repository.execute(tipologradouro_schema)

        # Retorno da informação
        return response