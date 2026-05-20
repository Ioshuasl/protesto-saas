from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_censec_tipoato.t_censec_tipoato_index_repository import (
    TCensecTipoAtoIndexRepository,
)


class TCensecTipoAtoIndexAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de todos os registros na tabela T_CENSEC_TIPOATO.
    """

    def execute(self):
        """
        Executa a operação de listagem no banco de dados.

        Args:
            t_censec_tipoato_index_schema (TCensecTipoAtoIndexSchema):
                Esquema contendo parâmetros opcionais de filtro.

        Returns:
            A lista de registros encontrados.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        t_censec_tipoato_index_repository = TCensecTipoAtoIndexRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = t_censec_tipoato_index_repository.execute()

        # ----------------------------------------------------
        # Retorno da informação
        # --------------------------------
        return response
