from packages.v1.administrativo.actions.t_servico_tipo.t_servico_tipo_top_servicos_tipo_action import (
    TopServicosTipoAction,
)


class TopServicosTipoService:

    def execute(self):
        return TopServicosTipoAction().execute()
