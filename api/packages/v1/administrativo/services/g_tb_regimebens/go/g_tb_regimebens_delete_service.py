from packages.v1.administrativo.schemas.g_tb_regimebens_schema import GTbRegimebensIdSchema
from packages.v1.administrativo.actions.g_tb_regimebens.g_tb_regimebens_delete_action import DeleteAction
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import DeleteService as SequenciaDeleteService


class DeleteService:

    def execute(self, regimebens_schema: GTbRegimebensIdSchema):

        # Instanciamento da ação
        delete_action = DeleteAction()

        # Executa a ação em questão
        data = delete_action.execute(regimebens_schema)

        # Validação de Sucesso: Só prossegue se 'data' for verdadeiro
        if data:
            # Instancia o serviço de sequência
            seq_service = SequenciaDeleteService()
            
            # Cria o schema de deleção para a G_SEQUENCIA
            sequencia_schema = GSequenciaDeleteSchema(
                sequencia=regimebens_schema.tb_regimebens_id,
                tabela='G_TB_REGIMEBENS'
            )

            # Executa a atualização da sequência
            seq_service.execute(sequencia_schema)
            
            return data