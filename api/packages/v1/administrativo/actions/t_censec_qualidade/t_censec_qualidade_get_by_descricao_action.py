from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.t_censec_qualidade_schema import TCensecQualidadeDescricaoSchema
from packages.v1.administrativo.repositories.t_censec_qualidade.t_censec_qualidade_get_by_descricao_repository import GetByDescricaoRepository


class GetByDescricaoAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela t_censec_qualidade por descrição.
    """

    def execute(self, censec_qualidade_schema: TCensecQualidadeDescricaoSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            censec_qualidade_schema (TCensecQualidadeDescricaoSchema): O esquema com a descrição a ser buscada.

        Returns:
            O registro encontrado ou None.
        """
        # Instanciamento do repositório
        show_repository = GetByDescricaoRepository()

        # Execução do repositório
        response = show_repository.execute(censec_qualidade_schema)

        # Retorno da informação
        return response