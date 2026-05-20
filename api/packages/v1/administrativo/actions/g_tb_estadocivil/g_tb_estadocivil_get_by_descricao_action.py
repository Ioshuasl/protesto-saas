from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.g_tb_estadocivil_schema import GTbEstadoCivilDescricaoSchema
from packages.v1.administrativo.repositories.g_tb_estadocivil.g_tb_estadocivil_get_by_descricao_repository import GetByDescricaoRepository


class GetByDescricaoAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela g_tb_estadocivil por descrição.
    """

    def execute(self, estadocivil_schema: GTbEstadoCivilDescricaoSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            estadocivil_schema (GTbEstadoCivilDescricaoSchema): O esquema com a descrição a ser buscada.

        Returns:
            O registro encontrado ou None.
        """
        # Instanciamento do repositório
        show_repository = GetByDescricaoRepository()

        # Execução do repositório
        response = show_repository.execute(estadocivil_schema)

        # Retorno da informação
        return response