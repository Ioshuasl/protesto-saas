from types import SimpleNamespace

from packages.v1.administrativo.actions.t_pessoa.t_pessoa_show_action import (
    TPessoaShowAction,
)
from packages.v1.administrativo.actions.t_servico_tipo.t_servico_tipo_show_action import (
    ShowAction,
)
from packages.v1.administrativo.schemas.t_pessoa_schema import TPessoaIdSchema
from packages.v1.administrativo.schemas.t_servico_tipo_schema import (
    TServicoTipoIdSchema,
)
from packages.v1.servicos.atos.actions.t_ato.t_ato_show_action import TAtoShowAction
from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoIdSchema
from packages.v1.servicos.balcao.actions.t_servico_itempedido.t_servico_itempedido_index_action import (
    TServicoItemPedidoIndexAction,
)
from packages.v1.servicos.balcao.schemas.t_servico_itempedido_schema import (
    TServicoItemIndexSchema,
)


class TServicoItemPedidoIndexService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de registros na tabela T_SERVICO_ITEMPEDIDO.
    """

    def execute(self, data: TServicoItemIndexSchema):
        t_servico_itempedido_index_action = TServicoItemPedidoIndexAction()
        # Execução da ação
        rows = t_servico_itempedido_index_action.execute(
            data
        )

        # Lista para armazenar os objetos convertidos e modificados
        data = []

        # Verifica se existe resultado
        if rows:

            for row in rows:

                # Cria o objeto mutável localmente
                item = SimpleNamespace(**row)

                # Montage da "subview" para o frontend:
                if getattr(item, "pessoa_id", None):

                    # Classe de busca de pessoa
                    pessoa_show_action = TPessoaShowAction()

                    # Monta a subview de acordo com a pessoa localizada
                    item.subview = pessoa_show_action.execute(
                        TPessoaIdSchema(pessoa_id=item.pessoa_id)
                    )

                    # Classe de busca de pessoa
                    servico_tipo_show = ShowAction()

                    # Monta a subview de acordo com a pessoa localizada
                    item.subview.servico_tipo = servico_tipo_show.execute(
                        TServicoTipoIdSchema(servico_tipo_id=item.servico_tipo_id)
                    )

                    # Atualiza o tipo item da subview
                    item.subview.servico_tipo.tipo_item = item.tipo_item

                # Montage da "subview" para o frontend:
                if getattr(item, "certidao_ato_id", None):

                    # Classe de busca de pessoa
                    ato_show_action = TAtoShowAction()

                    # Monta a subview de acordo com a pessoa localizada
                    item.subview = ato_show_action.execute(
                        TAtoIdSchema(ato_id=item.certidao_ato_id)
                    )

                    # Classe de busca de pessoa
                    servico_tipo_show = ShowAction()

                    # Monta a subview de acordo com a pessoa localizada
                    item.subview.servico_tipo = servico_tipo_show.execute(
                        TServicoTipoIdSchema(servico_tipo_id=item.servico_tipo_id)
                    )

                    # Atualiza o tipo item da subview
                    item.subview.servico_tipo.tipo_item = item.tipo_item

                    # Remove o texto
                    item.subview.texto = None

                # Remove os textos da resposta:
                item.certidao_texto = ""
                item.etiqueta_texto = ""

                # Adiciona o objeto processado na lista final
                data.append(item)
        return data
