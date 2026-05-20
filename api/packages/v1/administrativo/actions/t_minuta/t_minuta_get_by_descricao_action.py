from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.t_minuta_schema import TMinutaDescricaoSchema
from packages.v1.administrativo.repositories.t_minuta.t_minuta_get_by_descricao_repository import GetByDescricaoRepository


class GetByDescricaoAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela t_minuta por descrição.
    """

    def execute(self, minuta_schema: TMinutaDescricaoSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            minuta_schema (TMinutaDescricaoSchema): O esquema com a descrição a ser buscada.

        Returns:
            O registro encontrado ou None.
        """
        # Instanciamento do repositório
        show_repository = GetByDescricaoRepository()

        # Execução do repositório
        response = show_repository.execute(minuta_schema)

        # Retorno da informação
        return response