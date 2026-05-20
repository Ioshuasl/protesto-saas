from packages.v1.servicos.atos.actions.t_ato_parteimovel.t_ato_parteimovel_update_action import (
    TAtoParteImovelUpdateAction,
)
from packages.v1.servicos.atos.schemas.t_ato_parteimovel_schema import (
    TAtoParteImovelUpdateSchema,
)


class TAtoParteImovelUpdateService:
    """
    Serviço responsável pela operação de atualização de um registro
    na tabela T_ATO_PARTEIMOVEL.
    """

    def execute(self, t_ato_parteimovel_update_schema: TAtoParteImovelUpdateSchema):
        """
        Executa a operação de atualização no banco de dados.

        Args:
            t_ato_parteimovel_update_schema (TAtoParteImovelUpdateSchema):
                O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        t_ato_parteimovel_update_action = TAtoParteImovelUpdateAction()

        # ----------------------------------------------------
        # Execução da ação e retorno do resultado
        # ----------------------------------------------------
        return t_ato_parteimovel_update_action.execute(
            t_ato_parteimovel_update_schema
        )
