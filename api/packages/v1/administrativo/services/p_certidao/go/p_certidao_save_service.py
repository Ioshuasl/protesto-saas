from packages.v1.administrativo.actions.p_certidao.p_certidao_save_action import (
    SaveAction,
)
from packages.v1.administrativo.schemas.p_certidao_schema import PCertidaoSaveSchema
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService


class SaveService:
    def execute(self, certidao_schema: PCertidaoSaveSchema):
        if not certidao_schema.certidao_id:
            sequencia_schema = GSequenciaSchema()
            sequencia_schema.tabela = "P_CERTIDAO"
            certidao_schema.certidao_id = GenerateService().execute(
                sequencia_schema
            ).sequencia

        return SaveAction().execute(certidao_schema)
