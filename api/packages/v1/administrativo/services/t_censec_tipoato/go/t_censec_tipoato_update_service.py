from packages.v1.administrativo.actions.t_censec_tipoato.t_censec_tipoato_update_action import (
    TCensecTipoAtoUpdateAction,
)
from packages.v1.administrativo.schemas.t_censec_tipoato_schema import (
    TCensecTipoAtoUpdateSchema,
)


class TCensecTipoAtoUpdateService:
    """
    Serviço responsável pela operação de atualização de um registro
    na tabela T_CENSEC_TIPOATO.
    """

    def execute(self, t_censec_tipoato_update_schema: TCensecTipoAtoUpdateSchema):
        """
        Executa a operação de atualização no banco de dados.

        Args:
            t_censec_tipoato_update_schema (TCensecTipoAtoUpdateSchema):
                O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        t_censec_tipoato_update_action = TCensecTipoAtoUpdateAction()

        # ----------------------------------------------------
        # Execução da ação e retorno do resultado
        # ----------------------------------------------------
        return t_censec_tipoato_update_action.execute(t_censec_tipoato_update_schema)
