from abstracts.action import BaseAction

# Ajuste do schema de entrada
from packages.v1.administrativo.schemas.g_marcacao_tipo_schema import (
    GMarcacaoTipoSaveSchema,
)

# Ajuste do repositório
from packages.v1.administrativo.repositories.g_marcacao_tipo.g_marcacao_tipo_save_repository import (
    GMarcacaoTipoSaveRepository,
)


class GMarcacaoTipoSaveAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de salvar um novo registro na tabela G_MARCACAO_TIPO.
    """

    def execute(self, marcacao_tipo_schema: GMarcacaoTipoSaveSchema):
        """
        Executa a operação de salvamento.

        Args:
            marcacao_tipo_schema (GMarcacaoTipoSaveSchema): O esquema com os dados a serem salvos.

        Returns:
            O resultado da operação de salvamento.
        """
        # Instanciamento do repositório
        save_repository = GMarcacaoTipoSaveRepository()

        # Execução do repositório
        response = save_repository.execute(marcacao_tipo_schema)

        # Retorno da informação
        return response
