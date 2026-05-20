# Importação do Schema ajustada
from packages.v1.administrativo.schemas.g_marcacao_tipo_schema import (
    GMarcacaoTipoUpdateSchema,
)

# Importação do Repositório ajustada
from packages.v1.administrativo.repositories.g_marcacao_tipo.g_marcacao_tipo_update_repository import (
    GMarcacaoTipoUpdateRepository,
)


# A classe UpdateAction não herda de BaseAction no arquivo original, mantemos o padrão.
class GMarcacaoTipoUpdateAction:
    """
    Service responsável por encapsular a lógica de negócio para a atualização
    de um registro na tabela G_MARCACAO_TIPO.
    """

    def execute(self, marcacao_tipo_schema: GMarcacaoTipoUpdateSchema):
        """
        Executa a operação de atualização.

        Args:
            marcacao_tipo_id (int): O ID (MARCACAO_TIPO_ID) do registro a ser atualizado.
            marcacao_tipo_schema (GMarcacaoTipoUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # Instância o repositório de atualização
        update_repository = GMarcacaoTipoUpdateRepository()

        # Chama o método de execução do repositório para realizar a atualização
        return update_repository.execute(marcacao_tipo_schema)
