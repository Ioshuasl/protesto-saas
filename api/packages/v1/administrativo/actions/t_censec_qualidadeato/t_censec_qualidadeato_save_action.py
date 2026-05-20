from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_censec_qualidadeato.t_censec_qualidadeato_save_repository import (
    TCensecQualidadeAtoSaveRepository,
)
from packages.v1.administrativo.schemas.t_censec_qualidadeato_schema import (
    TCensecQualidadeAtoSaveSchema,
)


class TCensecQualidadeAtoSaveAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de salvamento de um novo registro na tabela T_CENSEC_QUALIDADEATO.
    """

    def execute(self, t_censec_qualidadeato_save_schema: TCensecQualidadeAtoSaveSchema):
        """
        Executa a operação de salvamento.

        Args:
            t_censec_qualidadeato_save_schema (TCensecQualidadeAtoSaveSchema):
                O esquema com os dados a serem persistidos.

        Returns:
            O resultado da operação de salvamento.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        t_censec_qualidadeato_save_repository = TCensecQualidadeAtoSaveRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = t_censec_qualidadeato_save_repository.execute(
            t_censec_qualidadeato_save_schema
        )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return response
