from packages.v1.servicos.atos.actions.t_ato.t_ato_delete_action import (
    TAtoDeleteAction,
)
from packages.v1.servicos.atos.actions.t_ato.t_ato_show_action import (
    TAtoShowAction,
)
from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoIdSchema
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import (
    DeleteService as SequenciaDeleteService,
)


class TAtoDeleteService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de exclusão de um registro na tabela T_ATO.
    """

    def execute(self, t_ato_id_schema: TAtoIdSchema):
        """
        Executa a operação de exclusão do registro no banco de dados.

        Args:
            t_ato_id_schema (TAtoIdSchema):
                O esquema com o ID do registro a ser excluído.

        Returns:
            O resultado da operação de exclusão.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        t_ato_delete_action = TAtoDeleteAction()

        # ----------------------------------------------------
        # Valida existência (e levanta 404 se não existir)
        # ----------------------------------------------------
        show_action = TAtoShowAction()
        show_action.execute(t_ato_id_schema)

        # ----------------------------------------------------
        # Execução da ação
        # ----------------------------------------------------
        data = t_ato_delete_action.execute(t_ato_id_schema)

        # ----------------------------------------------------
        # Controle de sequência após delete
        # ----------------------------------------------------
        seq_service = SequenciaDeleteService()
        sequencia_schema = GSequenciaDeleteSchema(
            sequencia=int(t_ato_id_schema.ato_id),
            tabela="T_ATO",
        )
        seq_service.execute(sequencia_schema)

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return data
