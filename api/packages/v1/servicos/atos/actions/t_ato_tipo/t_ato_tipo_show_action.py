from abstracts.action import BaseAction
from packages.v1.servicos.atos.repositories.t_ato_tipo.t_ato_tipo_show_repository import (
    TAtoTipoShowRepository,
)
from packages.v1.servicos.atos.schemas.t_ato_tipo_schema import (
    TAtoTipoIdSchema,
)


class TAtoTipoShowAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a exibição
    de um registro na tabela G_NATUREZA_TITULO.
    """

    def execute(self, t_ato_tipo_id_schema: TAtoTipoIdSchema):
        """
        Executa a operação de exibição.

        Args:
            t_ato_tipo_id_schema (TAtoTipoIdSchema):
                O esquema com o ID do registro a ser exibido.

        Returns:
            O resultado da operação de exibição.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        t_ato_tipo_show_repository = TAtoTipoShowRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = t_ato_tipo_show_repository.execute(
            t_ato_tipo_id_schema
        )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return response
