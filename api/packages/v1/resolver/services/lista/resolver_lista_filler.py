from packages.v1.resolver.actions.lista.resolver_cartorio_cidade_action import (
    ResolverCartorioCidadeAction,
)
from packages.v1.resolver.actions.lista.resolver_data_atual_action import (
    ResolverDataAtual,
)
from packages.v1.resolver.actions.lista.resolver_data_hora_atual_action import (
    ResolverDataHoraAtual,
)


class ResolverListaFiller:

    # Define a lista de possibilidades
    actions = {
        "data_atual": ResolverDataAtual,
        "data_hora_atual": ResolverDataHoraAtual,
        "cartorio_cidade": ResolverCartorioCidadeAction,
    }

    def execute(self, data):

        # Busca a classe de acordo com o nome da marcação
        action_controller = self.actions.get(data.texto.nome)

        # Retorna o valor da execução
        return action_controller.execute()
