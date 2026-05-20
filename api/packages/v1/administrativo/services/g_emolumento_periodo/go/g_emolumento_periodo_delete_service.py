from packages.v1.administrativo.actions.g_emolumento_periodo.g_emolumento_periodo_delete_action import (
    GEmolumentoPeriodoDeleteAction,
)
from packages.v1.administrativo.schemas.g_emolumento_periodo_schema import (
    GEmolumentoPeriodoIdSchema,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import DeleteService as SequenciaDeleteService


class GEmolumentoPeriodoDeleteService:

    def execute(self, g_emolumento_periodo_id_schema: GEmolumentoPeriodoIdSchema):
        
        # Instanciamento da ação        
        g_emolumento_periodo_delete_action = GEmolumentoPeriodoDeleteAction()
        
        # Execução da ação        
        data = g_emolumento_periodo_delete_action.execute(
            g_emolumento_periodo_id_schema
        )

        # Validação de Sucesso: Só prossegue se 'data' for verdadeiro
        if data:
            # Instancia o serviço de sequência
            seq_service = SequenciaDeleteService()
            
            # Cria o schema de deleção para a G_SEQUENCIA
            sequencia_schema = GSequenciaDeleteSchema(
                sequencia=g_emolumento_periodo_id_schema.emolumento_periodo_id,
                tabela='G_EMOLUMENTO_PERIODO'
            )

            # Executa a atualização da sequência
            seq_service.execute(sequencia_schema)
            
            return data

