from packages.v1.administrativo.schemas.t_censec_naturezalitigio_schema import TCensecNaturezalitigioUpdateSchema
from packages.v1.administrativo.repositories.t_censec_naturezalitigio.t_censec_naturezalitigio_update_repository import UpdateRepository


class UpdateAction:
    """
        Service responsável por encapsular a lógica de negócio para a atualização
        de um registro na tabela t_censec_naturezalitigio.
    """

    def execute(self, censec_naturezalitigio_id: int, censec_naturezalitigio_schema: TCensecNaturezalitigioUpdateSchema):
        """
        Executa a operação de atualização.

        Args:
            censec_naturezalitigio_id (int): O ID do registro a ser atualizado.
            censec_naturezalitigio_schema (TCensecNaturezalitigioUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # Instância o repositório de atualização
        update_repository = UpdateRepository()

        # Chama o método de execução do repositório para realizar a atualização
        return update_repository.execute(censec_naturezalitigio_id, censec_naturezalitigio_schema)