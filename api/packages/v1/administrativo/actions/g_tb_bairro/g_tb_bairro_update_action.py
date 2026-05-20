from packages.v1.administrativo.schemas.g_tb_bairro_schema import GTbBairroUpdateSchema
from packages.v1.administrativo.repositories.g_tb_bairro.g_tb_bairro_update_repository import UpdateRepository


class UpdateAction:
    """
        Service responsável por encapsular a lógica de negócio para a atualização
        de um registro na tabela g_tb_bairro.
    """

    def execute(self, tb_bairro_id: int, bairro_schema: GTbBairroUpdateSchema):
        """
        Executa a operação de atualização.

        Args:
            tb_bairro_id (int): O ID do registro a ser atualizado.
            bairro_schema (GTbBairroUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # Instância o repositório de atualização
        update_repository = UpdateRepository()

        # Chama o método de execução do repositório para realizar a atualização
        return update_repository.execute(tb_bairro_id, bairro_schema)