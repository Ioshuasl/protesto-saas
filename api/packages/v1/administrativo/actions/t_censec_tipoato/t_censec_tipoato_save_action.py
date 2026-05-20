from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_censec_tipoato.t_censec_tipoato_save_repository import (
    TCensecTipoAtoSaveRepository,
)
from packages.v1.administrativo.schemas.t_censec_tipoato_schema import (
    TCensecTipoAtoSaveSchema,
)


class TCensecTipoAtoSaveAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de salvamento de um novo registro na tabela T_CENSEC_TIPOATO.
    """

    def execute(self, t_censec_tipoato_save_schema: TCensecTipoAtoSaveSchema):
        """
        Executa a operação de salvamento.

        Args:
            t_censec_tipoato_schema (TCensecTipoAtoSchema):
                O esquema com os dados a serem persistidos.

        Returns:
            O resultado da operação de salvamento.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        t_censec_tipoato_save_repository = TCensecTipoAtoSaveRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = t_censec_tipoato_save_repository.execute(
            t_censec_tipoato_save_schema
        )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return response
