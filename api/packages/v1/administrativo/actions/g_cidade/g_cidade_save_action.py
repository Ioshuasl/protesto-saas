from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.g_cidade_schema import GCidadeSaveSchema
from packages.v1.administrativo.repositories.g_cidade.g_cidade_save_repository import SaveRepository

class SaveAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de salvar (inserir ou atualizar) um registro na tabela G_CIDADE.
    """

    def execute(self, g_cidade_schema: GCidadeSaveSchema):
        """
        Executa a operação de salvamento.

        Args:
            g_cidade_schema (GCidadeSaveSchema): O esquema com os dados a serem salvos.

        Returns:
            O resultado da operação de salvamento.
        """
        # Instanciamento do repositório
        save_repository = SaveRepository()

        # Execução do repositório
        response = save_repository.execute(g_cidade_schema)

        # Retorno da informação
        return response