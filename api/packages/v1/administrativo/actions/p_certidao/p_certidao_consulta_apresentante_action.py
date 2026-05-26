from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.p_certidao.p_certidao_consulta_apresentante_repository import (
    ConsultaApresentanteRepository,
)
from packages.v1.administrativo.schemas.p_certidao_schema import (
    PCertidaoConsultaApresentanteSchema,
)


class ConsultaApresentanteAction(BaseAction):
    def execute(self, consulta_schema: PCertidaoConsultaApresentanteSchema):
        return ConsultaApresentanteRepository().execute(consulta_schema)
