from packages.v1.administrativo.schemas.g_natureza_schema import GNaturezaUpdateSchema
from packages.v1.administrativo.repositories.g_natureza.g_natureza_update_repository import UpdateRepository


class UpdateAction:
    """
        Service responsável por encapsular a lógica de negócio para a atualização
        de um registro na tabela g_natureza.
    """

    def execute(self, natureza_id: int, natureza_schema: GNaturezaUpdateSchema):
        """
        Executa a operação de atualização.

        Args:
            natureza_id (int): O ID do registro a ser atualizado.
            natureza_schema (GNaturezaUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # Instância o repositório de atualização
        update_repository = UpdateRepository()

        # Chama o método de execução do repositório para realizar a atualização
        return update_repository.execute(natureza_id, natureza_schema)