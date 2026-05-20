from packages.v1.administrativo.schemas.t_censec_schema import TCensecUpdateSchema
from packages.v1.administrativo.repositories.t_censec.t_censec_update_repository import UpdateRepository


class UpdateAction:
    """
        Service responsável por encapsular a lógica de negócio para a atualização
        de um registro na tabela t_censec.
    """

    def execute(self, censec_id: int, censec_schema: TCensecUpdateSchema):
        """
        Executa a operação de atualização.

        Args:
            censec_id (int): O ID do registro a ser atualizado.
            censec_schema (TCensecUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # Instância o repositório de atualização
        update_repository = UpdateRepository()

        # Chama o método de execução do repositório para realizar a atualização
        return update_repository.execute(censec_id, censec_schema)