from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.g_tb_profissao_schema import GTbProfissaoUpdateSchema
from packages.v1.administrativo.repositories.g_tb_profissao.g_tb_profissao_update_repository import UpdateRepository


class GTbProfissaoUpdateAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a atualização
    de um registro na tabela G_TB_PROFISSAO.
    """

    def execute(self, tb_profissao_id: float, profissao_schema: GTbProfissaoUpdateSchema):
        """
        Executa a operação de atualização.

        Args:
            tb_profissao_id (float): O ID da profissão a ser atualizada.
            profissao_schema (GTbProfissaoUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # Instância o repositório de atualização
        update_repository = UpdateRepository()

        # Chama o método de execução do repositório para realizar a atualização
        return update_repository.execute(tb_profissao_id, profissao_schema)