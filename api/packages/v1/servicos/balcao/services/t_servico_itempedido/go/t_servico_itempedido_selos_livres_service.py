from types import SimpleNamespace

from packages.v1.administrativo.actions.g_selo_livro.g_selo_livro_livre_quantidade_show_action import (
    GSeloLivroLivreQuantidadeShowAction,
)
from packages.v1.administrativo.schemas.g_selo_livro_schema import (
    GSeloLivroLivreSchema,
)
from packages.v1.servicos.balcao.actions.t_servico_itempedido.t_servico_itempedido_index_grouped_action import (
    TServicoItemPedidoIndexGroupedAction,
)
from packages.v1.servicos.balcao.schemas.t_servico_itempedido_schema import (
    TServicoItemIndexSchema,
)


class TServicoItemPedidoSelosLivresService:
    def execute(self, data: TServicoItemIndexSchema):
        rows = TServicoItemPedidoIndexGroupedAction().execute(data)
        result = []

        if rows:
            for row in rows:
                item = SimpleNamespace(**row)
                item.selos = GSeloLivroLivreQuantidadeShowAction().execute(
                    GSeloLivroLivreSchema(selo_grupo_id=item.selo_grupo_id)
                )
                result.append(item)

        return result
