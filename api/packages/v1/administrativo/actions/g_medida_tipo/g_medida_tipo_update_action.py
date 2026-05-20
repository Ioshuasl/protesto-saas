from packages.v1.administrativo.schemas.g_medida_tipo_schema import GMedidaTipoUpdateSchema
from packages.v1.administrativo.repositories.g_medida_tipo.g_medida_tipo_update_repository import UpdateRepository


class UpdateAction:
    """
        Service responsável por encapsular a lógica de negócio para a atualização
        de um registro na tabela g_medida_tipo.
    """

    def execute(self, medida_tipo_id: int, medida_tipo_schema: GMedidaTipoUpdateSchema):
        """
        Executa a operação de atualização.

        Args:
            medida_tipo_id (int): O ID do registro a ser atualizado.
            medida_tipo_schema (GMedidaTipoUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # Instância o repositório de atualização
        update_repository = UpdateRepository()

        # Chama o método de execução do repositório para realizar a atualização
        return update_repository.execute(medida_tipo_id, medida_tipo_schema)