from packages.v1.administrativo.actions.t_censec_qualidadeato.t_censec_qualidadeato_update_action import (
    TCensecQualidadeAtoUpdateAction,
)
from packages.v1.administrativo.schemas.t_censec_qualidadeato_schema import (
    TCensecQualidadeAtoUpdateSchema,
)


class TCensecQualidadeAtoUpdateService:
    """
    Serviço responsável pela operação de atualização de um registro
    na tabela T_CENSEC_QUALIDADEATO.
    """

    def execute(
        self, t_censec_qualidadeato_update_schema: TCensecQualidadeAtoUpdateSchema
    ):
        """
        Executa a operação de atualização no banco de dados.

        Args:
            t_censec_qualidadeato_update_schema (TCensecQualidadeAtoUpdateSchema):
                O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        t_censec_qualidadeato_update_action = TCensecQualidadeAtoUpdateAction()

        # ----------------------------------------------------
        # Execução da ação e retorno do resultado
        # ----------------------------------------------------
        return t_censec_qualidadeato_update_action.execute(
            t_censec_qualidadeato_update_schema
        )
