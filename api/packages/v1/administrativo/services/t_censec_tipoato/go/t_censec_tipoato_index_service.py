from packages.v1.administrativo.actions.t_censec_tipoato.t_censec_tipoato_index_action import (
    TCensecTipoAtoIndexAction,
)
from fastapi import HTTPException, status


class TCensecTipoAtoIndexService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de registros na tabela T_CENSEC_TIPOATO.
    """

    def execute(self):
        """
        Executa a operação de busca de todos os registros no banco de dados.

        Args:
            t_censec_tipoato_index_schema (TCensecTipoAtoIndexSchema):
                Esquema que pode conter filtros ou parâmetros de busca.

        Returns:
            A lista de registros encontrados.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        t_censec_tipoato_index_action = TCensecTipoAtoIndexAction()

        # ----------------------------------------------------
        # Execução da ação
        # ----------------------------------------------------
        data = t_censec_tipoato_index_action.execute()

        # ----------------------------------------------------
        # Verificação de retorno
        # ----------------------------------------------------
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar registros de T_CENSEC_TIPOATO.",
            )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return data
