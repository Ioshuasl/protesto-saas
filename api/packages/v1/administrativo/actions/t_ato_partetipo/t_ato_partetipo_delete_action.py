from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_ato_partetipo.t_ato_partetipo_delete_repository import (
    TAtoParteTipoDeleteRepository,
)
from packages.v1.administrativo.schemas.t_ato_partetipo_schema import (
    TAtoParteTipoIdSchema,
)


class TAtoParteTipoDeleteAction(BaseAction):

    def execute(self, t_ato_partetipo_id_schema: TAtoParteTipoIdSchema):

        # Instanciamento do repositório
        t_ato_partetipo_delete_repository = TAtoParteTipoDeleteRepository()

        # Execução do repositório
        response = t_ato_partetipo_delete_repository.execute(t_ato_partetipo_id_schema)

        return response
