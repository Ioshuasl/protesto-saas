from packages.v1.administrativo.schemas.g_tb_documentotipo_schema import GTbDocumentoTipoUpdateSchema
from packages.v1.administrativo.actions.g_tb_documentotipo.g_tb_documentotipo_update_action import UpdateAction

class UpdateService:
    """
    Serviço para a operação de atualização de um registro na tabela
    G_TB_DOCUMENTOTIPO.
    """
    def execute(self, tb_documentotipo_id : int, documentotipo_schema: GTbDocumentoTipoUpdateSchema):
        """
        Executa a operação de atualização no banco de dados.

        Args:
            documentotipo_schema (GtbDocumentotipoUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # Instanciamento de ações
        update_action = UpdateAction()

        # Retorna o resultado da operação
        return update_action.execute(tb_documentotipo_id, documentotipo_schema)