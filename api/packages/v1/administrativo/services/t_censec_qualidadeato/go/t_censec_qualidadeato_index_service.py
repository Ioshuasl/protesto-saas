from packages.v1.administrativo.actions.t_censec_qualidadeato.t_censec_qualidadeato_index_action import (
    TCensecQualidadeAtoIndexAction,
)
from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.t_censec_qualidadeato_schema import (
    TCensecQualidadeAtoIndexSchema,
)


class TCensecQualidadeAtoIndexService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de registros na tabela T_CENSEC_QUALIDADEATO.
    """

    def execute(
        self, censec_qualidade_ato_index_schema: TCensecQualidadeAtoIndexSchema
    ):
        """
        Executa a operação de busca de todos os registros no banco de dados.

        Returns:
            A lista de registros encontrados.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        t_censec_qualidadeato_index_action = TCensecQualidadeAtoIndexAction()

        # ----------------------------------------------------
        # Execução da ação
        # ----------------------------------------------------
        data = t_censec_qualidadeato_index_action.execute(
            censec_qualidade_ato_index_schema
        )

        # ----------------------------------------------------
        # Verificação de retorno
        # ----------------------------------------------------
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar registros de T_CENSEC_QUALIDADEATO.",
            )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return data
