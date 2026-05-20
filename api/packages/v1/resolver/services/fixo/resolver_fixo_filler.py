from packages.v1.resolver.actions.fixo.resolver_ato_outorgado_qualificacao import ResolverAtoOutorgadoQualificacao
from packages.v1.resolver.actions.fixo.resolver_ato_outorgante_qualificacao import ResolverAtoOutorganteQualificacao


class ResolverFixoFiller:

    # Define a lista de possibilidades
    actions = {
        "ato_outorgante_qualificacao": ResolverAtoOutorganteQualificacao,
        "ato_outorgado_qualificacao": ResolverAtoOutorgadoQualificacao,
        "ato_parte_tipo": ResolverAtoOutorgadoQualificacao,
    }

    def execute(self, data):

        # Busca a classe de acordo com o nome da marcação
        action_controller = self.actions.get(data.texto.nome)

        # Retorna o valor da execução
        return action_controller.execute(data)