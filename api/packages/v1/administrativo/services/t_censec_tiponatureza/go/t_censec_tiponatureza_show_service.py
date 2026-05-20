from packages.v1.administrativo.actions.t_censec_naturezatipo.t_censec_tiponatureza_show_action import (
    TCensecTipoNaturezaShowAction,
)
from packages.v1.administrativo.schemas.t_censec_tiponatureza_schema import (
    TCensecTipoNaturezaIdSchema,
)
from fastapi import HTTPException, status


class TCensecTipoNaturezaShowService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela T_CENSEC_TIPONATUREZA.
    """

    def execute(self, t_censec_tiponatureza_id_schema: TCensecTipoNaturezaIdSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            t_censec_tiponatureza_id_schema (TCensecTipoNaturezaIdSchema):
                O esquema com o ID do registro a ser buscado.

        Returns:
            O resultado da busca.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        t_censec_tiponatureza_show_action = TCensecTipoNaturezaShowAction()

        # ----------------------------------------------------
        # Execução da ação
        # ----------------------------------------------------
        data = t_censec_tiponatureza_show_action.execute(
            t_censec_tiponatureza_id_schema
        )

        # ----------------------------------------------------
        # Verificação de resultado
        # ----------------------------------------------------
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar o registro de T_CENSEC_TIPONATUREZA.",
            )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return data
