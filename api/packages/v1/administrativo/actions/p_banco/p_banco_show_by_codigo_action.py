from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_banco.p_banco_show_repository import (
    ShowRepository,
)
from packages.v1.administrativo.schemas.p_banco_schema import PBancoCodigoSchema


class ShowByCodigoAction(BaseAction):
    def execute(self, codigo_schema: PBancoCodigoSchema):
        return ShowRepository().execute_by_codigo(codigo_schema)
