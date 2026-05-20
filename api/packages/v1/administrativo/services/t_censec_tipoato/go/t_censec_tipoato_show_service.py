from packages.v1.administrativo.actions.t_censec_tipoato.t_censec_tipoato_show_action import (
    TCensecTipoAtoShowAction,
)
from packages.v1.administrativo.schemas.t_censec_tipoato_schema import (
    TCensecTipoAtoIdSchema,
)
from fastapi import HTTPException, status


class TCensecTipoAtoShowService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela T_CENSEC_TIPOATO.
    """

    def execute(self, t_censec_tipoato_id_schema: TCensecTipoAtoIdSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            t_censec_tipoato_id_schema (TCensecTipoAtoIdSchema):
                O esquema com o ID do registro a ser buscado.

        Returns:
            O resultado da busca.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        t_censec_tipoato_show_action = TCensecTipoAtoShowAction()

        # ----------------------------------------------------
        # Execução da ação
        # ----------------------------------------------------
        data = t_censec_tipoato_show_action.execute(t_censec_tipoato_id_schema)

        # ----------------------------------------------------
        # Verificação de resultado
        # ----------------------------------------------------
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar o registro de T_CENSEC_TIPOATO.",
            )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return data
