from fastapi import HTTPException, status
from packages.v1.administrativo.actions.t_tb_cartorio.t_tb_cartorio_show_action import TTbCartorioShowAction
from packages.v1.administrativo.schemas.t_tb_cartorio_schema import TTbCartorioIdSchema
class TTbCartorioShowService:
    def execute(self, cartorio_schema: TTbCartorioIdSchema):
        data = TTbCartorioShowAction().execute(cartorio_schema)
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nao foi possivel localizar o registro do cartorio.",
            )
        return data
