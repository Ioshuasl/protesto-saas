from abstracts.action import BaseAction
from packages.v1.servicos.atos.repositories.t_ato.t_ato_update_texto_assinatura_repository import (
    TAtoUpdateTextoAssinaturaRepository,
)
from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoTextoAssinaturaUpdateSchema


class TAtoUpdateTextoAssinaturaAction(BaseAction):
    """
    Action responsavel por encapsular a atualizacao do texto de assinatura.
    """

    def execute(self, data: TAtoTextoAssinaturaUpdateSchema):
        """
        Executa a operacao de atualizacao.
        """

        response = TAtoUpdateTextoAssinaturaRepository().execute(data)

        return response

