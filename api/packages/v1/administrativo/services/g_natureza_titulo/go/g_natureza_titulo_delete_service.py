from packages.v1.administrativo.actions.g_natureza_titulo.g_natureza_titulo_delete_action import (
    GNaturezaTituloDeleteAction,
)
from packages.v1.administrativo.schemas.g_natureza_titulo_schema import (
    GNaturezaTituloIdSchema,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import DeleteService as SequenciaDeleteService


class GNaturezaTituloDeleteService:

    def execute(self, g_natureza_titulo_id_schema: GNaturezaTituloIdSchema):

        
        # Instanciamento da ação        
        g_natureza_titulo_delete_action = GNaturezaTituloDeleteAction()
        
        # Execução da ação        
        data = g_natureza_titulo_delete_action.execute(g_natureza_titulo_id_schema)

        # Validação de Sucesso: Só prossegue se 'data' for verdadeiro
        if data:
            # Instancia o serviço de sequência
            seq_service = SequenciaDeleteService()
            
            # Cria o schema de deleção para a G_SEQUENCIA
            sequencia_schema = GSequenciaDeleteSchema(
                sequencia=g_natureza_titulo_id_schema.natureza_titulo_id,
                tabela='G_NATUREZA_TITULO'
            )

            # Executa a atualização da sequência
            seq_service.execute(sequencia_schema)
            
            return data
