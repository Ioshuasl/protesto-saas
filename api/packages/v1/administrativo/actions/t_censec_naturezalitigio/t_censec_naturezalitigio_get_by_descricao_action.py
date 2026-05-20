from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.t_censec_naturezalitigio_schema import TCensecNaturezalitigioDescricaoSchema
from packages.v1.administrativo.repositories.t_censec_naturezalitigio.t_censec_naturezalitigio_get_by_descricao_repository import GetByDescricaoRepository


class GetByDescricaoAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela t_censec_naturezalitigio por descrição.
    """

    def execute(self, censec_naturezalitigio_schema: TCensecNaturezalitigioDescricaoSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            censec_naturezalitigio_schema (TCensecNaturezalitigioDescricaoSchema): O esquema com a descrição a ser buscada.

        Returns:
            O registro encontrado ou None.
        """
        # Instanciamento do repositório
        show_repository = GetByDescricaoRepository()

        # Execução do repositório
        response = show_repository.execute(censec_naturezalitigio_schema)

        # Retorno da informação
        return response