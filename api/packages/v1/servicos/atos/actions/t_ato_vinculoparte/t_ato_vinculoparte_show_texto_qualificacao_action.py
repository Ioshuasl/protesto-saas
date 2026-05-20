from abstracts.action import BaseAction
from packages.v1.servicos.atos.repositories.t_ato_vinculoparte.t_ato_vinculoparte_show_texto_qualificacao_repository import (
    TAtoVinculoParteShowTextoQualificacaoRepository,
)
from packages.v1.servicos.atos.schemas.t_ato_vinculoparte_schema import (
    TAtoVinculoParteIdSchema,
)


class TAtoVinculoParteShowTextoQualificacaoAction(BaseAction):
    """
    Action para buscar TEXTO_QUALIFICACAO de um vínculo de parte.
    """

    def execute(self, data: TAtoVinculoParteIdSchema):
        return TAtoVinculoParteShowTextoQualificacaoRepository().execute(data)
