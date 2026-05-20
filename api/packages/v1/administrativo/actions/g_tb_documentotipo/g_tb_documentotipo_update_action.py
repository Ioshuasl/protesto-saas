from packages.v1.administrativo.schemas.g_tb_documentotipo_schema import GTbDocumentoTipoUpdateSchema
from packages.v1.administrativo.repositories.g_tb_documentotipo.g_tb_documentotipo_update_repository import UpdateRepository


class UpdateAction:
    """
        Service responsável por encapsular a lógica de negócio para a atualização
        de um registro na tabela g_tb_documentotipo.
    """

    def execute(self, documento_tipo_id: int, documento_tipo_schema: GTbDocumentoTipoUpdateSchema):
        """
        Executa a operação de atualização.

        Args:
            documento_tipo_id (int): O ID do registro a ser atualizado.
            documento_tipo_schema (GTbDocumentoTipoUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # Instância o repositório de atualização
        update_repository = UpdateRepository()

        # Chama o método de execução do repositório para realizar a atualização
        return update_repository.execute(documento_tipo_id, documento_tipo_schema)