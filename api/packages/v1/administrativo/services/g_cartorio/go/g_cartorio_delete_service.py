from packages.v1.administrativo.actions.g_cartorio.g_cartorio_delete_action import (
    GCartorioDeleteAction,
)
from packages.v1.administrativo.schemas.g_cartorio_schema import GCartorioIdSchema
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import DeleteService as SequenciaDeleteService


class GCartorioDeleteService:

    def execute(self, g_cartorio_id_schema: GCartorioIdSchema):

        # Instanciamento da ação        
        g_cartorio_delete_action = GCartorioDeleteAction()

        # Execução da ação
        data = g_cartorio_delete_action.execute(g_cartorio_id_schema)

        # Validação de Sucesso: Só prossegue se 'data' for verdadeiro
        if data:
            # Instancia o serviço de sequência
            seq_service = SequenciaDeleteService()
            
            # Cria o schema de deleção para a G_SEQUENCIA
            sequencia_schema = GSequenciaDeleteSchema(
                sequencia=g_cartorio_id_schema.cartorio_id,
                tabela='G_CARTORIO'
            )

            # Executa a atualização da sequência
            seq_service.execute(sequencia_schema)
            
            return data
