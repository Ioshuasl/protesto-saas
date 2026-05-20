from packages.v1.servicos.atos.actions.t_ato_andamento.t_ato_andamento_show_action import (
    TAtoAndamentoShowAction,
)
from packages.v1.servicos.atos.schemas.t_ato_andamento_schema import (
    TAtoAndamentoIdSchema,
)
from fastapi import HTTPException, status


class TAtoAndamentoShowService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela T_ATO_ANDAMENTO.
    """

    def execute(self, t_ato_andamento_id_schema: TAtoAndamentoIdSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            t_ato_andamento_id_schema (TAtoAndamentoIdSchema):
                O esquema com o ID do registro a ser buscado.

        Returns:
            O resultado da busca.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        t_ato_andamento_show_action = TAtoAndamentoShowAction()

        # ----------------------------------------------------
        # Execução da ação
        # ----------------------------------------------------
        data = t_ato_andamento_show_action.execute(t_ato_andamento_id_schema)

        # ----------------------------------------------------
        # Verificação de resultado
        # ----------------------------------------------------
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar o registro de T_ATO_ANDAMENTO.",
            )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return data
