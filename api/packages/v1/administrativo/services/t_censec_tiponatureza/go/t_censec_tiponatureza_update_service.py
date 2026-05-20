from packages.v1.administrativo.actions.t_censec_naturezatipo.t_censec_tiponatureza_update_action import (
    TCensecTipoNaturezaUpdateAction,
)
from packages.v1.administrativo.schemas.t_censec_tiponatureza_schema import (
    TCensecTipoNaturezaUpdateSchema,
)


class TCensecTipoNaturezaUpdateService:
    """
    Serviço responsável pela operação de atualização de um registro
    na tabela T_CENSEC_TIPONATUREZA.
    """

    def execute(
        self, t_censec_tiponatureza_update_schema: TCensecTipoNaturezaUpdateSchema
    ):
        """
        Executa a operação de atualização no banco de dados.

        Args:
            t_censec_tiponatureza_update_schema (TCensecTipoNaturezaUpdateSchema):
                O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        t_censec_tiponatureza_update_action = TCensecTipoNaturezaUpdateAction()

        # ----------------------------------------------------
        # Execução da ação e retorno do resultado
        # ----------------------------------------------------
        return t_censec_tiponatureza_update_action.execute(
            t_censec_tiponatureza_update_schema
        )
