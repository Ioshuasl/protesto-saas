from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.t_tb_andamentoservico_schema import TTbAndamentoservicoIdSchema
from packages.v1.administrativo.repositories.t_tb_andamentoservico.t_tb_andamentoservico_delete_repository import DeleteRepository


class DeleteAction(BaseAction):

    def execute(self, andamentoservico_schema: TTbAndamentoservicoIdSchema):

        # Instanciamento do repositório
        delete_repository = DeleteRepository()

        # Execução do repositório
        return delete_repository.execute(andamentoservico_schema)