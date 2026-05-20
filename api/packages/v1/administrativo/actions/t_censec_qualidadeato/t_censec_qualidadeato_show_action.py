from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_censec_qualidadeato.t_censec_qualidadeato_show_repository import (
    TCensecQualidadeAtoShowRepository,
)
from packages.v1.administrativo.schemas.t_censec_qualidadeato_schema import (
    TCensecQualidadeAtoIdSchema,
)


class TCensecQualidadeAtoShowAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a exibição
    de um registro na tabela T_CENSEC_QUALIDADEATO.
    """

    def execute(self, t_censec_qualidadeato_id_schema: TCensecQualidadeAtoIdSchema):
        """
        Executa a operação de exibição.

        Args:
            t_censec_qualidadeato_id_schema (TCensecQualidadeAtoIdSchema):
                O esquema com o ID do registro a ser exibido.

        Returns:
            O resultado da operação de exibição.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        t_censec_qualidadeato_show_repository = TCensecQualidadeAtoShowRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = t_censec_qualidadeato_show_repository.execute(
            t_censec_qualidadeato_id_schema
        )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return response
