from abstracts.action import BaseAction

# Ajuste do schema de entrada
from packages.v1.administrativo.schemas.g_marcacao_tipo_schema import (
    GMarcacaoTipoIdSchema,
)

# Ajuste do repositório
from packages.v1.administrativo.repositories.g_marcacao_tipo.g_marcacao_tipo_show_repository import (
    GMarcacaoTipoShowRepository,
)


class GMarcacaoTipoShowAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a exibição
    de um registro na tabela G_MARCACAO_TIPO.
    """

    def execute(self, marcacao_tipo_schema: GMarcacaoTipoIdSchema):
        """
        Executa a operação de exibição.

        Args:
            marcacao_tipo_schema (GMarcacaoTipoIdSchema): O esquema com o ID (MARCACAO_TIPO_ID) do registro a ser exibido.

        Returns:
            O resultado da operação de exibição.
        """
        # Instânciamento do repositório
        show_repository = GMarcacaoTipoShowRepository()

        # Execução do repositório
        response = show_repository.execute(marcacao_tipo_schema)

        # Retorno da informação
        return response
