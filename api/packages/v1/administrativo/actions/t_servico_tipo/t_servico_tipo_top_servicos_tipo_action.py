from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_servico_tipo.t_servico_tipo_top_servicos_tipo_repository import (
    TopServicosTipoRepository,
)


class TopServicosTipoAction(BaseAction):

    def execute(self):
        return TopServicosTipoRepository().execute()
