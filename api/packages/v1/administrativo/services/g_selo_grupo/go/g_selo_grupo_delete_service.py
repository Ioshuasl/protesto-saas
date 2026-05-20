from packages.v1.administrativo.actions.g_selo_grupo.g_selo_grupo_delete_action import (
    GSeloGrupoDeleteAction,
)
from packages.v1.administrativo.schemas.g_selo_grupo_schema import GSeloGrupoIdSchema
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import DeleteService as SequenciaDeleteService


class GSeloGrupoDeleteService:

    def execute(self, g_selo_grupo_id_schema: GSeloGrupoIdSchema):
        
        # Instanciamento da ação        
        g_selo_grupo_delete_action = GSeloGrupoDeleteAction()
        
        # Execução da ação        
        data = g_selo_grupo_delete_action.execute(g_selo_grupo_id_schema)

        # Validação de Sucesso: Só prossegue se 'data' for verdadeiro
        if data:
            # Instancia o serviço de sequência
            seq_service = SequenciaDeleteService()
            
            # Cria o schema de deleção para a G_SEQUENCIA
            sequencia_schema = GSequenciaDeleteSchema(
                sequencia=g_selo_grupo_id_schema.selo_grupo_id,
                tabela='G_SELO_GRUPO'
            )

            # Executa a atualização da sequência
            seq_service.execute(sequencia_schema)
            
            return data
