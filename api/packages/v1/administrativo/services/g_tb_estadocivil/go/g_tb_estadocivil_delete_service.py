from packages.v1.administrativo.schemas.g_tb_estadocivil_schema import GTbEstadoCivilIdSchema
from packages.v1.administrativo.actions.g_tb_estadocivil.g_tb_estadocivil_delete_action import DeleteAction
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import DeleteService as SequenciaDeleteService


class DeleteService:

    def execute(self, estado_civil_schema: GTbEstadoCivilIdSchema):

        # Instanciamento da ação
        delete_action = DeleteAction()

        # Executa a ação em questão
        data = delete_action.execute(estado_civil_schema)

        # Validação de Sucesso: Só prossegue se 'data' for verdadeiro
        if data:
            # Instancia o serviço de sequência
            seq_service = SequenciaDeleteService()
            
            # Cria o schema de deleção para a G_SEQUENCIA
            sequencia_schema = GSequenciaDeleteSchema(
                sequencia=estado_civil_schema.tb_estadocivil_id,
                tabela='G_TB_ESTADOCIVIL'
            )

            # Executa a atualização da sequência
            seq_service.execute(sequencia_schema)
            
            return data