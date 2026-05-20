from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.t_tb_andamentoservico_schema import TTbAndamentoservicoDescricaoSchema
from packages.v1.administrativo.repositories.t_tb_andamentoservico.t_tb_andamentoservico_get_by_descricao_repository import GetByDescricaoRepository

class GetByDescricaoAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela t_tb_andamentoservico por descrição.
    """

    def execute(self, andamentoservico_schema: TTbAndamentoservicoDescricaoSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            andamentoservico_schema (TTbAndamentoservicoDescricaoSchema): O esquema com a descrição a ser buscada.

        Returns:
            O registro encontrado ou None.
        """
        # Instanciamento do repositório
        show_repository = GetByDescricaoRepository()

        # Execução do repositório
        response = show_repository.execute(andamentoservico_schema)

        # Retorno da informação
        return response