from packages.v1.administrativo.schemas.t_servico_etiqueta_schema import TServicoEtiquetaUpdateSchema
from packages.v1.administrativo.repositories.t_servico_etiqueta.t_servico_etiqueta_update_repository import UpdateRepository


class UpdateAction:
    """
        Service responsável por encapsular a lógica de negócio para a atualização
        de um registro na tabela T_SERVICO_ETIQUETA.
    """

    def execute(self, servico_etiqueta_id: int, servico_etiqueta_schema: TServicoEtiquetaUpdateSchema):
        """
        Executa a operação de atualização.

        Args:
            servico_etiqueta_id (int): O ID (SERVICO_ETIQUETA_ID) do registro a ser atualizado.
            servico_etiqueta_schema (TServicoEtiquetaUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # Instância o repositório de atualização
        update_repository = UpdateRepository()

        # Chama o método de execução do repositório para realizar a atualização
        return update_repository.execute(servico_etiqueta_id, servico_etiqueta_schema)