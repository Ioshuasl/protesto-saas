from abstracts.action import BaseAction
from packages.v1.servicos.atos.repositories.t_ato_vinculoimovel.t_ato_vinculoimovel_delete_repository import (
    TAtoVinculoImovelDeleteRepository,
)
from packages.v1.servicos.atos.schemas.t_ato_vinculoimovel_schema import (
    TAtoVinculoImovelIdSchema,
)


class TAtoVinculoImovelDeleteAction(BaseAction):

    def execute(self, t_ato_vinculoimovel_id_schema: TAtoVinculoImovelIdSchema):

        # Instância da classe
        t_ato_vinculoimovel_delete_repository = TAtoVinculoImovelDeleteRepository()

        # Executa a ação
        return t_ato_vinculoimovel_delete_repository.execute(
            t_ato_vinculoimovel_id_schema
        )
