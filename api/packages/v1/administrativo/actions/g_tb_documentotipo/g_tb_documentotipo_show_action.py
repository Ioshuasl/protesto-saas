from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.g_tb_documentotipo_schema import GTbDocumentoTipoIdSchema
from packages.v1.administrativo.repositories.g_tb_documentotipo.g_tb_documentotipo_show_repository import ShowRepository

class ShowAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a exibição
    de um registro na tabela g_tb_documentotipo.
    """

    def execute(self, documento_tipo_schema: GTbDocumentoTipoIdSchema):
        """
        Executa a operação de exibição.
        
        Args:
            documento_tipo_schema (GTbDocumentoTipoIdSchema): O esquema com o ID do registro a ser exibido.

        Returns:
            O resultado da operação de exibição.
        """
        # Instanciamento do repositório
        show_repository = ShowRepository()

        # Execução do repositório
        response = show_repository.execute(documento_tipo_schema)

        # Retorno da informação
        return response