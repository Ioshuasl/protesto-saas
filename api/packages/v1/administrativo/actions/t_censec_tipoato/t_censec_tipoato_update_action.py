from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_censec_tipoato.t_censec_tipoato_update_repository import (
    TCensecTipoAtoUpdateRepository,
)
from packages.v1.administrativo.schemas.t_censec_tipoato_schema import (
    TCensecTipoAtoUpdateSchema,
)


class TCensecTipoAtoUpdateAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a atualização
    de um registro na tabela T_CENSEC_TIPOATO.
    """

    def execute(self, t_censec_tipoato_update_schema: TCensecTipoAtoUpdateSchema):
        """
        Executa a operação de atualização.

        Args:
            t_censec_tipoato_update_schema (TCensecTipoAtoUpdateSchema):
                O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório de atualização
        # ----------------------------------------------------
        t_censec_tipoato_update_repository = TCensecTipoAtoUpdateRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = t_censec_tipoato_update_repository.execute(
            t_censec_tipoato_update_schema
        )

        # ----------------------------------------------------
        # Retorno do resultado
        # ----------------------------------------------------
        return response
