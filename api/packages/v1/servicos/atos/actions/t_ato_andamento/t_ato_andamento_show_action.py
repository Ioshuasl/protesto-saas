from abstracts.action import BaseAction
from packages.v1.servicos.atos.repositories.t_ato_andamento.t_ato_andamento_show_repository import (
    TAtoAndamentoShowRepository,
)
from packages.v1.servicos.atos.schemas.t_ato_andamento_schema import (
    TAtoAndamentoIdSchema,
)


class TAtoAndamentoShowAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a exibição
    de um registro na tabela G_NATUREZA_TITULO.
    """

    def execute(self, t_ato_andamento_id_schema: TAtoAndamentoIdSchema):
        """
        Executa a operação de exibição.

        Args:
            t_ato_andamento_id_schema (TAtoAndamentoIdSchema):
                O esquema com o ID do registro a ser exibido.

        Returns:
            O resultado da operação de exibição.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        t_ato_andamento_show_repository = TAtoAndamentoShowRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = t_ato_andamento_show_repository.execute(
            t_ato_andamento_id_schema
        )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return response
