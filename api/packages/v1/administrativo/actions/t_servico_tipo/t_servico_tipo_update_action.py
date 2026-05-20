from packages.v1.administrativo.schemas.t_servico_tipo_schema import TServicoTipoUpdateSchema
from packages.v1.administrativo.repositories.t_servico_tipo.t_servico_tipo_update_repository import UpdateRepository


class UpdateAction:
    """
        Service responsável por encapsular a lógica de negócio para a atualização
        de um registro na tabela T_SERVICO_TIPO.
    """

    def execute(self, servico_tipo_id: int, servico_tipo_schema: TServicoTipoUpdateSchema):
        """
        Executa a operação de atualização.

        Args:
            servico_tipo_id (int): O ID (SERVICO_TIPO_ID) do registro a ser atualizado.
            servico_tipo_schema (TServicoTipoUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # Instância o repositório de atualização
        update_repository = UpdateRepository()

        # Chama o método de execução do repositório para realizar a atualização
        return update_repository.execute(servico_tipo_id, servico_tipo_schema)