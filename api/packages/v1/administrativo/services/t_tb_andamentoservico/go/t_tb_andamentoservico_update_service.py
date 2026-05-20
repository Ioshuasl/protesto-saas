from packages.v1.administrativo.schemas.t_tb_andamentoservico_schema import TTbAndamentoservicoUpdateSchema
from packages.v1.administrativo.actions.t_tb_andamentoservico.t_tb_andamentoservico_update_action import UpdateAction

class TTbAndamentoservicoUpdateService:
    """
    Serviço para a operação de atualização de um registro na tabela
    t_tb_andamentoservico.
    """
    def execute(self, tb_andamentoservico_id : int, andamentoservico_schema: TTbAndamentoservicoUpdateSchema):
        """
        Executa a operação de atualização no banco de dados.

        Args:
            andamentoservico_schema (TTbAndamentoservicoUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # Instanciamento de ações
        update_action = UpdateAction()

        # Retorna o resultado da operação
        return update_action.execute(tb_andamentoservico_id, andamentoservico_schema)