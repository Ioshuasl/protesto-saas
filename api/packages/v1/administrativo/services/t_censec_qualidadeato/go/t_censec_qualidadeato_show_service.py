from packages.v1.administrativo.actions.t_censec_qualidadeato.t_censec_qualidadeato_show_action import (
    TCensecQualidadeAtoShowAction,
)
from packages.v1.administrativo.schemas.t_censec_qualidadeato_schema import (
    TCensecQualidadeAtoIdSchema,
)
from fastapi import HTTPException, status


class TCensecQualidadeAtoShowService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela T_CENSEC_QUALIDADEATO.
    """

    def execute(self, t_censec_qualidadeato_id_schema: TCensecQualidadeAtoIdSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            t_censec_qualidadeato_id_schema (TCensecQualidadeAtoIdSchema):
                O esquema com o ID do registro a ser buscado.

        Returns:
            O resultado da busca.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        t_censec_qualidadeato_show_action = TCensecQualidadeAtoShowAction()

        # ----------------------------------------------------
        # Execução da ação
        # ----------------------------------------------------
        data = t_censec_qualidadeato_show_action.execute(
            t_censec_qualidadeato_id_schema
        )

        # ----------------------------------------------------
        # Verificação de resultado
        # ----------------------------------------------------
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar o registro de T_CENSEC_QUALIDADEATO.",
            )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return data
