from packages.v1.administrativo.actions.p_titulo.p_titulo_save_action import SaveAction
from packages.v1.administrativo.schemas.p_titulo_schema import PTituloSaveSchema
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService


class SaveService:
    def execute(self, titulo_schema: PTituloSaveSchema):
        if not titulo_schema.titulo_id:
            sequencia_schema = GSequenciaSchema()
            sequencia_schema.tabela = "P_TITULO"
            titulo_schema.titulo_id = GenerateService().execute(sequencia_schema).sequencia

        return SaveAction().execute(titulo_schema)
