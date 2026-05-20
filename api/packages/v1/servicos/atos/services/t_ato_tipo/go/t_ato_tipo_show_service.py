from packages.v1.servicos.atos.actions.t_ato_tipo.t_ato_tipo_show_action import (
    TAtoTipoShowAction,
)
from packages.v1.servicos.atos.schemas.t_ato_tipo_schema import (
    TAtoTipoIdSchema,
)
from fastapi import HTTPException, status


class TAtoTipoShowService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela T_ATO_TIPO.
    """

    def execute(self, t_ato_tipo_id_schema: TAtoTipoIdSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            t_ato_tipo_id_schema (TAtoTipoIdSchema):
                O esquema com o ID do registro a ser buscado.

        Returns:
            O resultado da busca.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        t_ato_tipo_show_action = TAtoTipoShowAction()

        # ----------------------------------------------------
        # Execução da ação
        # ----------------------------------------------------
        data = t_ato_tipo_show_action.execute(t_ato_tipo_id_schema)

        # ----------------------------------------------------
        # Verificação de resultado
        # ----------------------------------------------------
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar o registro de T_ATO_TIPO.",
            )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return data
