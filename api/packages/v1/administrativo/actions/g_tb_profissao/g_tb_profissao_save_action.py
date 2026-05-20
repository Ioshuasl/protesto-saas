from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.g_tb_profissao_schema import GTbProfissaoSaveSchema
from packages.v1.administrativo.repositories.g_tb_profissao.g_tb_profissao_save_repository import SaveRepository

class GTbProfissaoSaveAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de salvar um novo registro na tabela G_TB_PROFISSAO.
    """

    def execute(self, profissao_schema: GTbProfissaoSaveSchema):
        """
        Executa a operação de salvamento.
        
        Args:
            profissao_schema (GTbProfissaoSaveSchema): O esquema com os dados a serem salvos.

        Returns:
            O resultado da operação de salvamento.
        """
        # Instanciamento do repositório
        save_repository = SaveRepository()

        # Execução do repositório
        response = save_repository.execute(profissao_schema)

        # Retorno da informação
        return response