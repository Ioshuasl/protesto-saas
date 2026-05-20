from abstracts.action import BaseAction

# Ajuste do schema de entrada
from packages.v1.administrativo.repositories.g_marcacao_tipo.g_marcacao_tipo_get_by_nome_repository7 import (
    GMarcacaoTipoGetByNomeRepository,
)
from packages.v1.administrativo.schemas.g_marcacao_tipo_schema import (
    GMarcacaoTipoNomeSchema,
)


class GetByNomeAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela G_MARCACAO_TIPO por descrição.
    """

    def execute(self, marcacao_tipo_schema: GMarcacaoTipoNomeSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            marcacao_tipo_schema (GMarcacaoTipoDescricaoSchema): O esquema com a descrição a ser buscada.

        Returns:
            O registro encontrado ou None.
        """
        # Instanciamento do repositório
        show_repository = GMarcacaoTipoGetByNomeRepository()

        # Execução do repositório
        response = show_repository.execute(marcacao_tipo_schema)

        # Retorno da informação
        return response
