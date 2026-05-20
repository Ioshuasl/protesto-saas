from packages.v1.administrativo.schemas.g_tb_regimecomunhao_schema import GTbRegimecomunhaoUpdateSchema
from packages.v1.administrativo.repositories.g_tb_regimecomunhao.g_tb_regimecomunhao_update_repository import UpdateRepository


class UpdateAction:
    """
        Service responsável por encapsular a lógica de negócio para a atualização
        de um registro na tabela g_tb_regimecomunhao.
    """

    def execute(self, tb_regimecomunhao_id : int, regimecomunhao_schema: GTbRegimecomunhaoUpdateSchema):
        """
        Executa a operação de atualização.

        Args:
            regimecomunhao_schema (GTbRegimecomunhaoUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # Instância o repositório de atualização
        update_repository = UpdateRepository()

        # Chama o método de execução do repositório para realizar a atualização
        return update_repository.execute(tb_regimecomunhao_id, regimecomunhao_schema)