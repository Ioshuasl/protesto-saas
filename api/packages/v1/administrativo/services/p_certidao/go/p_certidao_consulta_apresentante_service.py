from packages.v1.administrativo.actions.p_certidao.p_certidao_consulta_apresentante_action import (
    ConsultaApresentanteAction,
)
from packages.v1.administrativo.schemas.p_certidao_schema import (
    PCertidaoConsultaApresentanteSchema,
)


class ConsultaApresentanteService:
    def execute(self, consulta_schema: PCertidaoConsultaApresentanteSchema):
        return ConsultaApresentanteAction().execute(consulta_schema)
