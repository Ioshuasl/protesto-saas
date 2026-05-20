from abstracts.action import BaseAction
from packages.v1.servicos.atos.repositories.t_ato.t_ato_get_texto_corpo_repository import TAtoGetTextoCorpoRepository
from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoIdSchema


class TAtoGetTextoCorpoAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a exibição
    de um registro na tabela G_NATUREZA_TITULO.
    """

    def execute(self, data: TAtoIdSchema):
        """
        Executa a operação de exibição.

        Args:
            t_ato_id_schema (TAtoIdSchema):
                O esquema com o ID do registro a ser exibido.

        Returns:
            O resultado da operação de exibição.
        """
        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = TAtoGetTextoCorpoRepository().execute(data)

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return response
