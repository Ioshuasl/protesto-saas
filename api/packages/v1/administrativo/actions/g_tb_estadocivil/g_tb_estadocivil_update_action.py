from packages.v1.administrativo.schemas.g_tb_estadocivil_schema import GTbEstadoCivilUpdateSchema
from packages.v1.administrativo.repositories.g_tb_estadocivil.g_tb_estadocivil_update_repository import UpdateRepository


class UpdateAction:
    """
        Service responsável por encapsular a lógica de negócio para a atualização
        de um registro na tabela g_tb_estadocivil.
    """

    def execute(self, tb_estadocivil_id: int, estadocivil_schema: GTbEstadoCivilUpdateSchema):
        """
        Executa a operação de atualização.

        Args:
            tb_estadocivil_id (int): O ID do registro a ser atualizado.
            estadocivil_schema (GTbEstadoCivilUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # Instância o repositório de atualização
        update_repository = UpdateRepository()

        # Chama o método de execução do repositório para realizar a atualização
        return update_repository.execute(tb_estadocivil_id, estadocivil_schema)