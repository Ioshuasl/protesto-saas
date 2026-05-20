from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.g_tb_documentotipo_schema import GTbDocumentoTipoDescricaoSchema
from packages.v1.administrativo.repositories.g_tb_documentotipo.g_tb_documentotipo_get_by_descricao_repository import GetByDescricaoRepository


class GetByDescricaoAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela g_tb_documentotipo por descrição.
    """

    def execute(self, documento_tipo_schema: GTbDocumentoTipoDescricaoSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            documento_tipo_schema (GTbDocumentoTipoDescricaoSchema): O esquema com a descrição a ser buscada.

        Returns:
            O registro encontrado ou None.
        """
        # Instanciamento do repositório
        show_repository = GetByDescricaoRepository()

        # Execução do repositório
        response = show_repository.execute(documento_tipo_schema)

        # Retorno da informação
        return response