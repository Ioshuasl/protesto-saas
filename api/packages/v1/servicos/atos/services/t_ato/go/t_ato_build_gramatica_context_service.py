from packages.v1.servicos.atos.actions.t_ato_vinculoimovel.t_ato_vinculoimovel_index_action import (
    TAtoVinculoImovelIndexAction,
)
from packages.v1.servicos.atos.actions.t_ato_vinculoparte.t_ato_vinculoparte_index_by_tipo_vinculo_action import (
    TAtoVinculoParteIndexByTipoVinculoAction,
)
from packages.v1.servicos.atos.schemas.t_ato_vinculoimovel_schema import (
    TAtoVinculoImovelIndexSchema,
)
from packages.v1.servicos.atos.schemas.t_ato_vinculoparte_schema import (
    TAtoVinculoParteIndexByTipoVinculoSchema,
)


class TAtoBuildGramaticaContextService:
    def execute(self, ato_id):
        vinculo_parte_action = TAtoVinculoParteIndexByTipoVinculoAction()
        vinculo_imovel_action = TAtoVinculoImovelIndexAction()
        context = {}

        for role_name, tipo_vinculo in {"outorgante": 1, "outorgado": 2}.items():
            partes = vinculo_parte_action.execute(
                TAtoVinculoParteIndexByTipoVinculoSchema(
                    ato_id=ato_id,
                    tipo_vinculo=tipo_vinculo,
                )
            )
            if not partes:
                continue

            sexos = []
            for parte in partes:
                sexo = (getattr(parte, "pessoa_sexo", None) or "").strip().upper()
                if sexo in ("M", "F"):
                    sexos.append(sexo)

            context[role_name] = {
                "quantity": len(partes),
                "sexos": sexos,
            }

        imoveis = vinculo_imovel_action.execute(
            TAtoVinculoImovelIndexSchema(
                ato_id=ato_id,
            )
        )
        if imoveis:
            context["imoveis"] = {"quantity": len(imoveis)}

        return context
