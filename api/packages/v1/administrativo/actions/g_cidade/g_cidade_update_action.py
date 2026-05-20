from packages.v1.administrativo.schemas.g_cidade_schema import GCidadeUpdateSchema
from packages.v1.administrativo.repositories.g_cidade.g_cidade_update_repository import UpdateRepository


class UpdateAction:
    """
        Serviço responsável por encapsular a lógica de negócio para a atualização
        de um registro na tabela G_CIDADE.
    """

    def execute(self, cidade_id: int, g_cidade_schema: GCidadeUpdateSchema):
        """
        Executa a operação de atualização.

        Args:
            cidade_id (int): O ID (CIDADE_ID) do registro a ser atualizado.
            g_cidade_schema (GCidadeUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # Instância o repositório de atualização
        update_repository = UpdateRepository()

        # Chama o método de execução do repositório para realizar a atualização
        return update_repository.execute(cidade_id, g_cidade_schema)