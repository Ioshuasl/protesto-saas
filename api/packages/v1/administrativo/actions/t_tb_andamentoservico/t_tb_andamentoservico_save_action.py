from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.t_tb_andamentoservico_schema import TTbAndamentoservicoSaveSchema
from packages.v1.administrativo.repositories.t_tb_andamentoservico.t_tb_andamentoservico_save_repository import SaveRepository

class SaveAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de salvar um novo registro na tabela t_tb_andamentoservico.
    """

    def execute(self, andamentoservico_schema: TTbAndamentoservicoSaveSchema):
        """
        Executa a operação de salvamento.
        
        Args:
            andamentoservico_schema (TTbAndamentoservicoSaveSchema): O esquema com os dados a serem salvos.

        Returns:
            O resultado da operação de salvamento.
        """
        # Instânciamento do repositório
        save_repository = SaveRepository()

        # Execução do repositório
        response = save_repository.execute(andamentoservico_schema)

        # Retorno da informação
        return response