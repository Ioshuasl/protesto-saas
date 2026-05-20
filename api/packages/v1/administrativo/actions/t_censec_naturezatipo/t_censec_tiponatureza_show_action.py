from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_censec_tiponatureza.t_censec_tiponatureza_show_repository import (
    TCensecTipoNaturezaShowRepository,
)
from packages.v1.administrativo.schemas.t_censec_tiponatureza_schema import (
    TCensecTipoNaturezaIdSchema,
)


class TCensecTipoNaturezaShowAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a exibição
    de um registro na tabela T_CENSEC_TIPOATO.
    """

    def execute(self, t_censec_tiponatureza_id_schema: TCensecTipoNaturezaIdSchema):
        """
        Executa a operação de exibição.

        Args:
            t_censec_tiponatureza_id_schema (TCensecTipoNaturezaIdSchema):
                O esquema com o ID do registro a ser exibido.

        Returns:
            O resultado da operação de exibição.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        t_censec_tiponatureza_show_repository = TCensecTipoNaturezaShowRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = t_censec_tiponatureza_show_repository.execute(
            t_censec_tiponatureza_id_schema
        )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return response
