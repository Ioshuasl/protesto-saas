from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.t_minuta_schema import TMinutaUpdateSchema
from packages.v1.administrativo.repositories.t_minuta.t_minuta_update_repository import UpdateRepository


class UpdateAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a atualização
    de um registro na tabela t_minuta.
    """

    def execute(self, minuta_id: int, minuta_schema: TMinutaUpdateSchema):
        """
        Executa a operação de atualização.

        Args:
            minuta_id (int): O ID do registro a ser atualizado.
            minuta_schema (TMinutaUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # Instância o repositório de atualização
        update_repository = UpdateRepository()

        # Chama o método de execução do repositório para realizar a atualização
        return update_repository.execute(minuta_id, minuta_schema)