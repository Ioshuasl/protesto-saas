from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService
from packages.v1.servicos.atos.actions.t_historico.t_historico_save_action import (
    THistoricoSaveAction,
)
from packages.v1.servicos.atos.schemas.t_historico_schema import (
    THistoricoSaveSchema,
)


class THistoricoSaveService:
    """
    Serviço responsável por encapsular a lógica de negócio
    para criação de um registro em T_HISTORICO
    """

    def execute(self, data: THistoricoSaveSchema):

        # ----------------------------------------------------
        # Geração automática de ID (sequência)
        # ----------------------------------------------------
        if not data.historico_id:

            # Cria o schema de sequência
            sequencia_schema = GSequenciaSchema()
            sequencia_schema.tabela = "T_HISTORICO"

            # Gera a sequência atualizada
            generate = GenerateService()
            sequencia = generate.execute(sequencia_schema)

            # Atualiza o ID no schema
            data.historico_id = sequencia.sequencia

        action = THistoricoSaveAction()
        return action.execute(data)
