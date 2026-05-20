from packages.v1.servicos.atos.actions.t_ato_vinculoparte.t_ato_vinculoparte_show_action import (
    TAtoVinculoParteShowAction,
)
from packages.v1.servicos.atos.schemas.t_ato_vinculoparte_schema import (
    TAtoVinculoParteIdSchema,
)
from fastapi import HTTPException, status


class TAtoVinculoParteShowService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela T_ATO_VINCULOPARTE.
    """

    def execute(self, t_ato_vinculoparte_id_schema: TAtoVinculoParteIdSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            t_ato_vinculoparte_id_schema (TAtoVinculoParteIdSchema):
                O esquema com o ID do registro a ser buscado.

        Returns:
            O resultado da busca.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        t_ato_vinculoparte_show_action = TAtoVinculoParteShowAction()

        # ----------------------------------------------------
        # Execução da ação
        # ----------------------------------------------------
        data = t_ato_vinculoparte_show_action.execute(t_ato_vinculoparte_id_schema)

        # ----------------------------------------------------
        # Verificação de resultado
        # ----------------------------------------------------
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar o registro de T_ATO_VINCULOPARTE.",
            )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return data
