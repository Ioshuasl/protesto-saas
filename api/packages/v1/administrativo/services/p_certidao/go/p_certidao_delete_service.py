from packages.v1.administrativo.actions.p_certidao.p_certidao_delete_action import (
    DeleteAction,
)
from packages.v1.administrativo.actions.p_certidao.p_certidao_show_action import (
    ShowAction,
)
from packages.v1.administrativo.schemas.p_certidao_schema import PCertidaoIdSchema
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import (
    DeleteService as SequenciaDeleteService,
)


class DeleteService:
    def execute(self, certidao_schema: PCertidaoIdSchema):
        ShowAction().execute(certidao_schema)
        data = DeleteAction().execute(certidao_schema)

        if data:
            sequencia_schema = GSequenciaDeleteSchema(
                sequencia=certidao_schema.certidao_id,
                tabela="P_CERTIDAO",
            )
            SequenciaDeleteService().execute(sequencia_schema)

        return data
