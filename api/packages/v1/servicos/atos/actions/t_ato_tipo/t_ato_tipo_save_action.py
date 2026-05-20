from abstracts.action import BaseAction
from packages.v1.servicos.atos.repositories.t_ato_tipo.t_ato_tipo_save_repository import (
    TAtoTipoSaveRepository,
)
from packages.v1.servicos.atos.schemas.t_ato_tipo_schema import (
    TAtoTipoSaveSchema,
)


class TAtoTipoSaveAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de salvamento de um novo registro na tabela T_ATO_TIPO.
    """

    def execute(self, t_ato_tipo_save_schema: TAtoTipoSaveSchema):
        """
        Executa a operação de salvamento.

        Args:
            t_ato_tipo_schema (TAtoTipoSchema):
                O esquema com os dados a serem persistidos.

        Returns:
            O resultado da operação de salvamento.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        t_ato_tipo_save_repository = TAtoTipoSaveRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = t_ato_tipo_save_repository.execute(
            t_ato_tipo_save_schema
        )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return response
