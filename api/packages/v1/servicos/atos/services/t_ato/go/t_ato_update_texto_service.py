from packages.v1.servicos.atos.actions.t_ato.t_ato_update_texto_action import TAtoUpdateTextoAction
from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoUpdateTextoSchema

class TAtoUpdateTextoService:
    """
    Serviço responsável pela operação de atualização de um registro
    na tabela T_ATO.
    """

    def execute(self, data: TAtoUpdateTextoSchema):

        # ----------------------------------------------------
        # Execução da ação e retorno do resultado
        # ----------------------------------------------------
        return TAtoUpdateTextoAction().execute(data)
