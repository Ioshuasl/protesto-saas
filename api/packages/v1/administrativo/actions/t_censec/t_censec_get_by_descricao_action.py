from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.t_censec_schema import TCensecDescricaoSchema
from packages.v1.administrativo.repositories.t_censec.t_censec_get_by_descricao_repository import GetByDescricaoRepository


class GetByDescricaoAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela t_censec por descrição.
    """

    def execute(self, censec_schema: TCensecDescricaoSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            censec_schema (TCensecDescricaoSchema): O esquema com a descrição a ser buscada.

        Returns:
            O registro encontrado ou None.
        """
        # Instanciamento do repositório
        show_repository = GetByDescricaoRepository()

        # Execução do repositório
        response = show_repository.execute(censec_schema)

        # Retorno da informação
        return response