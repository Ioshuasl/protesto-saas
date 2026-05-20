from fastapi import HTTPException, status

from packages.v1.administrativo.actions.t_censec_naturezatipo.t_censec_tiponatureza_index_action import (
    TCensecTipoNaturezaIndexAction,
)


class TCensecTipoNaturezaIndexService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de registros na tabela T_CENSEC_TIPONATUREZA.
    """

    def execute(self):
        """
        Executa a operação de busca de todos os registros no banco de dados.

        Args:
            t_censec_tiponatureza_index_schema (TCensecTipoNaturezaIndexSchema):
                Esquema que pode conter filtros ou parâmetros de busca.

        Returns:
            A lista de registros encontrados.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        t_censec_tiponatureza_index_action = TCensecTipoNaturezaIndexAction()

        # ----------------------------------------------------
        # Execução da ação
        # ----------------------------------------------------
        data = t_censec_tiponatureza_index_action.execute()

        # ----------------------------------------------------
        # Verificação de retorno
        # ----------------------------------------------------
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar registros de T_CENSEC_TIPONATUREZA.",
            )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return data
