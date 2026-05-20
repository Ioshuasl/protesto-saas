from fastapi import HTTPException, status

from packages.v1.administrativo.actions.t_tb_sinal_publico.t_tb_sinal_publico_get_by_descricao_action import (
    TTbSinalPublicoGetByDescricaoAction,
)
from packages.v1.administrativo.schemas.t_tb_sinal_publico_schema import (
    TTbSinalPublicoDescricaoSchema,
)


class TTbSinalPublicoGetByDescricaoService:
    def execute(self, sinal_publico_schema: TTbSinalPublicoDescricaoSchema, messageValidate: bool):
        action = TTbSinalPublicoGetByDescricaoAction()
        data = action.execute(sinal_publico_schema)

        if messageValidate and not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nao foi possivel localizar o registro de sinal publico",
            )

        return data
