from packages.v1.administrativo.schemas.g_tb_tipologradouro_schema import GTbTipoLogradouroUpdateSchema
from packages.v1.administrativo.repositories.g_tb_tipologradouro.g_tb_tipologradouro_update_repository import UpdateRepository


class UpdateAction:
    """
        Serviço responsável por encapsular a lógica de negócio para a atualização
        de um registro na tabela g_tb_tipologradouro.
    """

    def execute(self, tipologradouro_id: int, tipologradouro_schema: GTbTipoLogradouroUpdateSchema):
        """
        Executa a operação de atualização.

        Args:
            tipologradouro_id (int): O ID do registro a ser atualizado.
            tipologradouro_schema (GTbTipologradouroUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # Instância o repositório de atualização
        update_repository = UpdateRepository()

        # Chama o método de execução do repositório para realizar a atualização
        return update_repository.execute(tipologradouro_id, tipologradouro_schema)