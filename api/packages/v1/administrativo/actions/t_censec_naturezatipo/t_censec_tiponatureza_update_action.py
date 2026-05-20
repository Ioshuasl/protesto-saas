from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_censec_tiponatureza.t_censec_tiponatureza_update_repository import (
    TCensecTipoNaturezaUpdateRepository,
)
from packages.v1.administrativo.schemas.t_censec_tiponatureza_schema import (
    TCensecTipoNaturezaUpdateSchema,
)


class TCensecTipoNaturezaUpdateAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a atualização
    de um registro na tabela T_CENSEC_TIPOATO.
    """

    def execute(
        self, t_censec_tiponatureza_update_schema: TCensecTipoNaturezaUpdateSchema
    ):
        """
        Executa a operação de atualização.

        Args:
            t_censec_tiponatureza_update_schema (TCensecTipoNaturezaUpdateSchema):
                O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório de atualização
        # ----------------------------------------------------
        t_censec_tiponatureza_update_repository = TCensecTipoNaturezaUpdateRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = t_censec_tiponatureza_update_repository.execute(
            t_censec_tiponatureza_update_schema
        )

        # ----------------------------------------------------
        # Retorno do resultado
        # ----------------------------------------------------
        return response
