from abstracts.action import BaseAction
from packages.v1.servicos.atos.uow.t_ato.t_ato_lavrar_ato_uow import (
    TAtoLavrarAtoUow,
)
from packages.v1.servicos.atos.schemas.t_ato_lavrar_ato_uow_schema import (
    TAtoLavrarAtoUowSchema,
)


class TAtoLavrarAtoUowAction(BaseAction):
    def execute(self, data: TAtoLavrarAtoUowSchema):
        return TAtoLavrarAtoUow().execute(data)
