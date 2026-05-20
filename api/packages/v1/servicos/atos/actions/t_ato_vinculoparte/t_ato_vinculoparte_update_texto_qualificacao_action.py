from abstracts.action import BaseAction
from packages.v1.servicos.atos.repositories.t_ato_vinculoparte.t_ato_vinculoparte_update_texto_qualificacao_repository import (
    TAtoVinculoParteUpdateTextoQualificacaoRepository,
)
from packages.v1.servicos.atos.schemas.t_ato_vinculoparte_schema import (
    TAtoVinculoParteTextoQualificacaoUpdateSchema,
)


class TAtoVinculoParteUpdateTextoQualificacaoAction(BaseAction):
    """
    Action para atualizar TEXTO_QUALIFICACAO de um vínculo de parte.
    """

    def execute(self, data: TAtoVinculoParteTextoQualificacaoUpdateSchema):
        return TAtoVinculoParteUpdateTextoQualificacaoRepository().execute(data)
