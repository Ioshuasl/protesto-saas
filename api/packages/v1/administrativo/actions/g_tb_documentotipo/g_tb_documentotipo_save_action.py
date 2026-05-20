from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.g_tb_documentotipo_schema import GTbDocumentoTipoSaveSchema
from packages.v1.administrativo.repositories.g_tb_documentotipo.g_tb_documentotipo_save_repository import SaveRepository

class SaveAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de salvar um novo registro na tabela g_tb_documentotipo.
    """

    def execute(self, documento_tipo_schema: GTbDocumentoTipoSaveSchema):
        """
        Executa a operação de salvamento.

        Args:
            documento_tipo_schema (GTbDocumentoTipoSaveSchema): O esquema com os dados a serem salvos.

        Returns:
            O resultado da operação de salvamento.
        """
        # Instanciamento do repositório
        save_repository = SaveRepository()

        # Execução do repositório
        response = save_repository.execute(documento_tipo_schema)

        # Retorno da informação
        return response