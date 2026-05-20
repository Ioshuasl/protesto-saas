from packages.v1.administrativo.schemas.g_tb_regimebens_schema import GTbRegimebensUpdateSchema
from packages.v1.administrativo.repositories.g_tb_regimebens.g_tb_regimebens_update_repository import UpdateRepository


class UpdateAction:
    """
        Service responsável por encapsular a lógica de negócio para a atualização
        de um registro na tabela g_tb_regimebens.
    """

    def execute(self, tb_regimebens_id: int, regimebens_schema: GTbRegimebensUpdateSchema):
        """
        Executa a operação de atualização.

        Args:
        regimebens_schema (GTbRegimebensUpdateSchema): O esquema com os dados a serem atualizados.

            Returns:
                O resultado da operação de atualização.
            """
        # Instância o repositório de atualização
        update_repository = UpdateRepository()

        # Chama o método de execução do repositório para realizar a atualização
        return update_repository.execute(tb_regimebens_id, regimebens_schema)