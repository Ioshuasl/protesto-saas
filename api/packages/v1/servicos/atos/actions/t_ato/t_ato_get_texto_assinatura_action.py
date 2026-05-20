from abstracts.action import BaseAction
from packages.v1.servicos.atos.repositories.t_ato.t_ato_get_texto_assinatura_repository import (
    TAtoGetTextoAssinaturaRepository,
)
from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoTextoAssinatura


class TAtoGetTextoAssinaturaAction(BaseAction):
    """
    Action responsavel por encapsular a exibicao do texto de assinatura.
    """

    def execute(self, data: TAtoTextoAssinatura):
        """
        Executa a operacao de exibicao.
        """
        response = TAtoGetTextoAssinaturaRepository().execute(data)

        return response

