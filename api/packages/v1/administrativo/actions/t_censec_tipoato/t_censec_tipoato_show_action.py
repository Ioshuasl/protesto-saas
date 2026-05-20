from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_censec_tipoato.t_censec_tipoato_show_repository import (
    TCensecTipoAtoShowRepository,
)
from packages.v1.administrativo.schemas.t_censec_tipoato_schema import (
    TCensecTipoAtoIdSchema,
)


class TCensecTipoAtoShowAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a exibição
    de um registro na tabela T_CENSEC_TIPOATO.
    """

    def execute(self, t_censec_tipoato_id_schema: TCensecTipoAtoIdSchema):
        """
        Executa a operação de exibição.

        Args:
            t_censec_tipoato_id_schema (TCensecTipoAtoIdSchema):
                O esquema com o ID do registro a ser exibido.

        Returns:
            O resultado da operação de exibição.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        t_censec_tipoato_show_repository = TCensecTipoAtoShowRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = t_censec_tipoato_show_repository.execute(t_censec_tipoato_id_schema)

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return response
