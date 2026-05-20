from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.g_tb_regimecomunhao_schema import GTbRegimecomunhaoSaveSchema
from packages.v1.administrativo.repositories.g_tb_regimecomunhao.g_tb_regimecomunhao_save_repository import SaveRepository


class SaveAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de salvar um novo registro na tabela g_tb_regimecomunhao.
    """

    def execute(self, regimecomunhao_schema: GTbRegimecomunhaoSaveSchema):
        """
        Executa a operação de salvamento.

        Args:
            regimecomunhao_schema (GTbRegimecomunhaoSaveSchema): O esquema com os dados a serem salvos.

        Returns:
            O resultado da operação de salvamento.
        """
        # Instânciamento do repositório
        save_repository = SaveRepository()

        # Execução do repositório
        response = save_repository.execute(regimecomunhao_schema)

        # Retorno da informação
        return response