from packages.v1.administrativo.actions.p_arquivo_titulo.p_arquivo_titulo_save_action import (
    SaveAction,
)
from packages.v1.administrativo.schemas.p_arquivo_titulo_schema import PArquivoTituloSaveSchema
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService


class SaveService:
    def execute(self, arquivo_schema: PArquivoTituloSaveSchema):
        if not arquivo_schema.arquivo_titulo_id:
            sequencia_schema = GSequenciaSchema()
            sequencia_schema.tabela = "P_ARQUIVO_TITULO"
            arquivo_schema.arquivo_titulo_id = GenerateService().execute(
                sequencia_schema
            ).sequencia

        return SaveAction().execute(arquivo_schema)
