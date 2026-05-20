from packages.v1.administrativo.actions.g_gramatica.g_gramatica_delete_action import (
    GGramaticaDeleteAction,
)
from packages.v1.administrativo.schemas.g_gramatica_schema import GGramaticaIdSchema
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import DeleteService as SequenciaDeleteService


class GGramaticaDeleteService:

    def execute(self, g_gramatica_id_schema: GGramaticaIdSchema):
        
        # Instanciamento da ação        
        g_gramatica_delete_action = GGramaticaDeleteAction()
        
        # Execução da ação        
        data = g_gramatica_delete_action.execute(g_gramatica_id_schema)

        # Validação de Sucesso: Só prossegue se 'data' for verdadeiro
        if data:
            # Instancia o serviço de sequência
            seq_service = SequenciaDeleteService()
            
            # Cria o schema de deleção para a G_SEQUENCIA
            sequencia_schema = GSequenciaDeleteSchema(
                sequencia=g_gramatica_id_schema.gramatica_id,
                tabela='G_GRAMATICA'
            )

            # Executa a atualização da sequência
            seq_service.execute(sequencia_schema)
            
            return data
