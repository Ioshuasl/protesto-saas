from types import SimpleNamespace
from packages.v1.servicos.atos.actions.t_ato.t_ato_show_action import (
    TAtoShowAction,
)
from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoIdSchema
from fastapi import HTTPException, status


class TAtoShowService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela T_ATO.
    """

    def execute(self, t_ato_id_schema: TAtoIdSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            t_ato_id_schema (TAtoIdSchema):
                O esquema com o ID do registro a ser buscado.

        Returns:
            O resultado da busca.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        t_ato_show_action = TAtoShowAction()

        # ----------------------------------------------------
        # Execução da ação
        # ----------------------------------------------------
        data = t_ato_show_action.execute(t_ato_id_schema)

        # ----------------------------------------------------
        # Verificação de resultado
        # ----------------------------------------------------
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nao encontramos o ato informado. Verifique o codigo e tente novamente.",
            )

        # Clona o objeto
        item = SimpleNamespace(**data)

        # Limpa o campo de texto
        item.texto = None

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return item
