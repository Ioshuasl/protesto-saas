from fastapi import HTTPException, status

from packages.v1.administrativo.actions.t_tb_sinal_publico.t_tb_sinal_publico_show_action import (
    TTbSinalPublicoShowAction,
)
from packages.v1.administrativo.schemas.t_tb_sinal_publico_schema import (
    TTbSinalPublicoIdSchema,
)


class TTbSinalPublicoShowService:
    def execute(self, sinal_publico_schema: TTbSinalPublicoIdSchema):
        show_action = TTbSinalPublicoShowAction()
        data = show_action.execute(sinal_publico_schema)

        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nao foi possivel localizar o registro de sinal publico",
            )

        return data
