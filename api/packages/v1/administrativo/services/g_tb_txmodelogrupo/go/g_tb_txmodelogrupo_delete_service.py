from packages.v1.administrativo.schemas.g_tb_txmodelogrupo_schema import GTbTxmodelogrupoIdSchema
from packages.v1.administrativo.actions.g_tb_txmodelogrupo.g_tb_txmodelogrupo_delete_action import DeleteAction
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import DeleteService as SequenciaDeleteService


class DeleteService:
    
    def execute(self, txmodelogrupo_schema: GTbTxmodelogrupoIdSchema):
        
        # Instanciamento de ação
        delete_action = DeleteAction()

        # Executa a ação em questão
        data = delete_action.execute(txmodelogrupo_schema)

        # Validação de Sucesso: Só prossegue se 'data' for verdadeiro
        if data:
            # Instancia o serviço de sequência
            seq_service = SequenciaDeleteService()
            
            # Cria o schema de deleção para a G_SEQUENCIA
            sequencia_schema = GSequenciaDeleteSchema(
                sequencia=txmodelogrupo_schema.tb_txmodelogrupo_id,
                tabela='G_TB_TXMODELOGRUPO'
            )

            # Executa a atualização da sequência
            seq_service.execute(sequencia_schema)
            
            return data