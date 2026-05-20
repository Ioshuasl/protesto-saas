from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.t_tb_reconhecimentotipo_schema import TTbReconhecimentotipoSaveSchema
from packages.v1.administrativo.repositories.t_tb_reconhecimentotipo.t_tb_reconhecimentotipo_save_repository import SaveRepository

class SaveAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de salvar um novo registro na tabela t_tb_reconhecimentotipo.
    """

    def execute(self, reconhecimentotipo_schema: TTbReconhecimentotipoSaveSchema):
        """
        Executa a operação de salvamento.
        
        Args:
            reconhecimentotipo_schema (T_TbReconhecimentotipoSaveSchema): O esquema com os dados a serem salvos.

        Returns:
            O resultado da operação de salvamento.
        """
        # Instânciamento do repositório
        save_repository = SaveRepository()

        # Execução do repositório
        response = save_repository.execute(reconhecimentotipo_schema)

        # Retorno da informação
        return response
