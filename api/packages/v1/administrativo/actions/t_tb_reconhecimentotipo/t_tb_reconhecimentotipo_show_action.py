from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.t_tb_reconhecimentotipo_schema import TTbReconhecimentotipoIdSchema
from packages.v1.administrativo.repositories.t_tb_reconhecimentotipo.t_tb_reconhecimentotipo_show_repository import ShowRepository

class ShowAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a exibição
    de um registro na tabela t_tb_reconhecimentotipo.
    """

    def execute(self, reconhecimentotipo_schema: TTbReconhecimentotipoIdSchema):
        """
        Executa a operação de exibição.
        
        Args:
            reconhecimentotipo_schema (T_TbReconhecimentotipoIdSchema): O esquema com o ID do registro a ser exibido.

        Returns:
            O resultado da operação de exibição.
        """
        # Instânciamento do repositório
        show_repository = ShowRepository()

        # Execução do repositório
        response = show_repository.execute(reconhecimentotipo_schema)

        # Retorno da informação
        return response
