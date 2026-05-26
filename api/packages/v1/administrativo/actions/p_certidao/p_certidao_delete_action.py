from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_certidao.p_certidao_delete_repository import (
    DeleteRepository,
)
from packages.v1.administrativo.schemas.p_certidao_schema import PCertidaoIdSchema


class DeleteAction(BaseAction):
    def execute(self, certidao_schema: PCertidaoIdSchema):
        return DeleteRepository().execute(certidao_schema)
