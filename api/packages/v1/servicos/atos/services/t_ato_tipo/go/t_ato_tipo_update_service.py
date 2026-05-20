from packages.v1.servicos.atos.actions.t_ato_tipo.t_ato_tipo_update_action import (
    TAtoTipoUpdateAction,
)
from packages.v1.servicos.atos.schemas.t_ato_tipo_schema import (
    TAtoTipoUpdateSchema,
)


class TAtoTipoUpdateService:
    """
    Serviço responsável pela operação de atualização de um registro
    na tabela T_ATO_TIPO.
    """

    def execute(self, t_ato_tipo_update_schema: TAtoTipoUpdateSchema):
        """
        Executa a operação de atualização no banco de dados.

        Args:
            t_ato_tipo_update_schema (TAtoTipoUpdateSchema):
                O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        t_ato_tipo_update_action = TAtoTipoUpdateAction()

        # ----------------------------------------------------
        # Execução da ação e retorno do resultado
        # ----------------------------------------------------
        return t_ato_tipo_update_action.execute(
            t_ato_tipo_update_schema
        )
