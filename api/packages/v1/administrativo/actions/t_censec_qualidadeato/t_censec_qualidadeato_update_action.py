from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_censec_qualidadeato.t_censec_qualidadeato_update_repository import (
    TCensecQualidadeAtoUpdateRepository,
)
from packages.v1.administrativo.schemas.t_censec_qualidadeato_schema import (
    TCensecQualidadeAtoUpdateSchema,
)


class TCensecQualidadeAtoUpdateAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a atualização
    de um registro na tabela T_CENSEC_QUALIDADEATO.
    """

    def execute(
        self, t_censec_qualidadeato_update_schema: TCensecQualidadeAtoUpdateSchema
    ):
        """
        Executa a operação de atualização.

        Args:
            t_censec_qualidadeato_update_schema (TCensecQualidadeAtoUpdateSchema):
                O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório de atualização
        # ----------------------------------------------------
        t_censec_qualidadeato_update_repository = TCensecQualidadeAtoUpdateRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = t_censec_qualidadeato_update_repository.execute(
            t_censec_qualidadeato_update_schema
        )

        # ----------------------------------------------------
        # Retorno do resultado
        # ----------------------------------------------------
        return response
