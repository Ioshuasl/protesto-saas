from packages.v1.administrativo.schemas.g_tb_profissao_schema import GTbProfissaoUpdateSchema
from packages.v1.administrativo.actions.g_tb_profissao.g_tb_profissao_update_action import GTbProfissaoUpdateAction

class GTbProfissaoUpdateService:
    """
    Serviço para a operação de atualização de um registro na tabela
    G_TB_PROFISSAO.
    """
    def execute(self, tb_profissao_id : float, profissao_schema: GTbProfissaoUpdateSchema):
        """
        Executa a operação de atualização no banco de dados.

        Args:
            tb_profissao_id (float): O ID da profissão a ser atualizada.
            profissao_schema (GTbProfissaoUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # Instanciamento de ações
        update_action = GTbProfissaoUpdateAction()

        # Retorna o resultado da operação
        return update_action.execute(tb_profissao_id, profissao_schema)