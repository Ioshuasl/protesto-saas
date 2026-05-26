from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_certidao.p_certidao_cancelar_repository import (
    CancelarRepository,
)
from packages.v1.administrativo.schemas.p_certidao_schema import PCertidaoIdSchema


class CancelarAction(BaseAction):
    def execute(self, certidao_schema: PCertidaoIdSchema):
        return CancelarRepository().execute(certidao_schema)
