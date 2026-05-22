from packages.v1.administrativo.actions.p_motivos_cancelamento.p_motivos_cancelamento_save_action import (
    SaveAction,
)
from packages.v1.administrativo.schemas.p_motivos_cancelamento_schema import (
    PMotivosCancelamentoSaveSchema,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService


class SaveService:
    def execute(self, motivos_cancelamento_schema: PMotivosCancelamentoSaveSchema):
        if not motivos_cancelamento_schema.motivos_cancelamento_id:
            sequencia_schema = GSequenciaSchema()
            sequencia_schema.tabela = "P_MOTIVOS_CANCELAMENTO"
            motivos_cancelamento_schema.motivos_cancelamento_id = (
                GenerateService().execute(sequencia_schema).sequencia
            )

        return SaveAction().execute(motivos_cancelamento_schema)
