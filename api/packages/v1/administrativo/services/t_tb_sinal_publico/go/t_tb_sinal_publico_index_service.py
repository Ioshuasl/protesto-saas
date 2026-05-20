from fastapi import HTTPException, status

from packages.v1.administrativo.actions.t_tb_sinal_publico.t_tb_sinal_publico_index_action import (
    TTbSinalPublicoIndexAction,
)


class TTbSinalPublicoIndexService:
    def execute(self):
        index_action = TTbSinalPublicoIndexAction()
        data = index_action.execute()

        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nao foi possivel localizar os registros de sinal publico",
            )

        return data
