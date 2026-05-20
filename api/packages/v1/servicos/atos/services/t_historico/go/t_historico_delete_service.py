from packages.v1.servicos.atos.actions.t_historico.t_historico_delete_action import (
    THistoricoDeleteAction,
)
from packages.v1.servicos.atos.actions.t_historico.t_historico_show_action import (
    THistoricoShowAction,
)
from packages.v1.servicos.atos.schemas.t_historico_schema import (
    THistoricoIdSchema,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import (
    DeleteService as SequenciaDeleteService,
)


class DeleteService:
    pass


class THistoricoDeleteService:
    """
    Serviço responsável por encapsular a lógica de negócio
    para exclusão de um registro em T_HISTORICO
    """

    def execute(self, schema: THistoricoIdSchema):
        # ----------------------------------------------------
        # Valida existência (e levanta 404 se não existir)
        # ----------------------------------------------------
        show_action = THistoricoShowAction()
        show_action.execute(schema)

        action = THistoricoDeleteAction()

        data = action.execute(schema)

        # ----------------------------------------------------
        # Controle de sequência após delete
        # ----------------------------------------------------
        seq_service = SequenciaDeleteService()
        sequencia_schema = GSequenciaDeleteSchema(
            sequencia=int(schema.historico_id),
            tabela="T_HISTORICO",
        )
        seq_service.execute(sequencia_schema)

        return data
