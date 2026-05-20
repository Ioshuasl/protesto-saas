from abstracts.action import BaseAction
from packages.v1.servicos.atos.repositories.t_ato_andamento.t_ato_andamento_update_repository import (
    TAtoAndamentoUpdateRepository,
)
from packages.v1.servicos.atos.schemas.t_ato_andamento_schema import (
    TAtoAndamentoUpdateSchema,
)


class TAtoAndamentoUpdateAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a atualização
    de um registro na tabela G_NATUREZA_TITULO.
    """

    def execute(self, t_ato_andamento_update_schema: TAtoAndamentoUpdateSchema):
        """
        Executa a operação de atualização.

        Args:
            t_ato_andamento_update_schema (TAtoAndamentoUpdateSchema):
                O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório de atualização
        # ----------------------------------------------------
        t_ato_andamento_update_repository = TAtoAndamentoUpdateRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = t_ato_andamento_update_repository.execute(
            t_ato_andamento_update_schema
        )

        # ----------------------------------------------------
        # Retorno do resultado
        # ----------------------------------------------------
        return response
