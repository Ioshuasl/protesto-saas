from fastapi import HTTPException, status
from packages.v1.administrativo.schemas.g_tb_documentotipo_schema import GTbDocumentoTipoIdSchema
from packages.v1.administrativo.actions.g_tb_documentotipo.g_tb_documentotipo_show_action import ShowAction

class ShowService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela G_TB_DOCUMENTOTIPO.
    """

    def execute(self, documentotipo_schema: GTbDocumentoTipoIdSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            documentotipo_schema (GtbDocumentotipoIdSchema): O esquema com o ID a ser buscado.

        Returns:
            O resultado da busca.
        """
        # Instanciamento da ação
        show_action = ShowAction()

        # Executa a ação em questão
        data = show_action.execute(documentotipo_schema)

        if not data:
            # Retorna uma exceção
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Não foi possível localizar o registro de G_TB_DOCUMENTOTIPO'
            )

        # Retorno da informação
        return data