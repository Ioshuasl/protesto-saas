from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_censec_tiponatureza.t_censec_tiponatureza_save_repository import (
    TCensecTipoNaturezaSaveRepository,
)
from packages.v1.administrativo.schemas.t_censec_tiponatureza_schema import (
    TCensecTipoNaturezaSaveSchema,
)


class TCensecTipoNaturezaSaveAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de salvamento de um novo registro na tabela T_CENSEC_TIPOATO.
    """

    def execute(self, t_censec_tiponatureza_save_schema: TCensecTipoNaturezaSaveSchema):
        """
        Executa a operação de salvamento.

        Args:
            t_censec_tiponatureza_schema (TCensecTipoNaturezaSchema):
                O esquema com os dados a serem persistidos.

        Returns:
            O resultado da operação de salvamento.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        t_censec_tiponatureza_save_repository = TCensecTipoNaturezaSaveRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = t_censec_tiponatureza_save_repository.execute(
            t_censec_tiponatureza_save_schema
        )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return response
