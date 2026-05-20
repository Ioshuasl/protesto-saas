from abstracts.action import BaseAction

# Ajuste do schema de entrada
from packages.v1.administrativo.schemas.g_marcacao_tipo_schema import (
    GMarcacaoTipoGrupoSchema,
)

# Ajuste do repositório
from packages.v1.administrativo.repositories.g_marcacao_tipo.g_marcacao_tipo_get_by_grupo_repository import (
    GMarcacaoTipoGetByGrupoRepository,
)


class GMarcacaoTipoGetByGrupoAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela G_MARCACAO_TIPO por filtro.
    """

    def execute(self, marcacao_tipo_schema: GMarcacaoTipoGrupoSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            marcacao_tipo_schema (GMarcacaoTipoGrupoSchema): O esquema com os filtros a serem buscados.

        Returns:
            O registro encontrado ou None.
        """
        # Instanciamento do repositório
        show_repository = GMarcacaoTipoGetByGrupoRepository()

        # Execução do repositório
        response = show_repository.execute(marcacao_tipo_schema)

        # Retorno da informação
        return response
