from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.g_medida_tipo_schema import GMedidaTipoSaveSchema
from packages.v1.administrativo.repositories.g_medida_tipo.g_medida_tipo_save_repository import SaveRepository

class SaveAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de salvar um novo registro na tabela g_medida_tipo.
    """

    def execute(self, medida_tipo_schema: GMedidaTipoSaveSchema):
        """
        Executa a operação de salvamento.

        Args:
            medida_tipo_schema (GMedidaTipoSaveSchema): O esquema com os dados a serem salvos.

        Returns:
            O resultado da operação de salvamento.
        """
        # Instanciamento do repositório
        save_repository = SaveRepository()

        # Execução do repositório
        response = save_repository.execute(medida_tipo_schema)

        # Retorno da informação
        return response