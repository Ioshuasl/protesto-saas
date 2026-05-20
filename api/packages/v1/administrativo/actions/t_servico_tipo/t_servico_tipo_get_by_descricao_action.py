from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.t_servico_tipo_schema import TServicoTipoDescricaoSchema
from packages.v1.administrativo.repositories.t_servico_tipo.t_servico_tipo_get_by_descricao_repository import GetByDescricaoRepository


class GetByDescricaoAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela T_SERVICO_TIPO por descrição.
    """

    def execute(self, servico_tipo_schema: TServicoTipoDescricaoSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            servico_tipo_schema (TServicoTipoDescricaoSchema): O esquema com a descrição a ser buscada.

        Returns:
            O registro encontrado ou None.
        """
        # Instanciamento do repositório
        show_repository = GetByDescricaoRepository()

        # Execução do repositório
        response = show_repository.execute(servico_tipo_schema)

        # Retorno da informação
        return response