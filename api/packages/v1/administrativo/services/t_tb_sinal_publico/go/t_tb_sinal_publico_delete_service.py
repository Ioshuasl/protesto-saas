from fastapi import HTTPException, status

from packages.v1.administrativo.actions.t_tb_sinal_publico.t_tb_sinal_publico_delete_action import (
    TTbSinalPublicoDeleteAction,
)
from packages.v1.administrativo.actions.t_tb_sinal_publico.t_tb_sinal_publico_show_action import (
    TTbSinalPublicoShowAction,
)
from packages.v1.administrativo.schemas.t_tb_sinal_publico_schema import (
    TTbSinalPublicoIdSchema,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import (
    DeleteService as SequenciaDeleteService,
)


class TTbSinalPublicoDeleteService:
    def execute(self, sinal_publico_schema: TTbSinalPublicoIdSchema):
        show_action = TTbSinalPublicoShowAction()
        current_data = show_action.execute(sinal_publico_schema)

        if not current_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nao foi possivel localizar o registro de sinal publico",
            )

        delete_action = TTbSinalPublicoDeleteAction()
        data = delete_action.execute(sinal_publico_schema)

        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nao foi possivel excluir o registro ou ele nao existe.",
            )

        seq_service = SequenciaDeleteService()
        seq_service.execute(
            GSequenciaDeleteSchema(
                sequencia=sinal_publico_schema.tb_sinalpublico_id,
                tabela="T_TB_SINALPUBLICO",
            )
        )

        return data
