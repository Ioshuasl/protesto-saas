from fastapi import HTTPException, status
from packages.v1.administrativo.schemas.t_tb_andamentoservico_schema import TTbAndamentoservicoIdSchema
from packages.v1.administrativo.actions.t_tb_andamentoservico.t_tb_andamentoservico_show_action import ShowAction

class ShowService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela t_tb_andamentoservico.
    """

    def execute(self, andamentoservico_schema: TTbAndamentoservicoIdSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            andamentoservico_schema (TTbAndamentoservicoIdSchema): O esquema com o ID a ser buscado.

        Returns:
            O resultado da busca.
        """
        # Instanciamento da ação
        show_action = ShowAction()

        # Executa a ação em questão
        data = show_action.execute(andamentoservico_schema)

        if not data:
            # Retorna uma exceção
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Não foi possível localizar o registro de andamento de serviço'
            )

        # Retorno da informação
        return data