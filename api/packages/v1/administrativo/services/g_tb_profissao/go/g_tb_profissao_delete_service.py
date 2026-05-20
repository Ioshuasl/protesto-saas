from packages.v1.administrativo.schemas.g_tb_profissao_schema import GTbProfissaoIdSchema
from packages.v1.administrativo.actions.g_tb_profissao.g_tb_profissao_delete_action import GTbProfissaoDeleteAction
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import DeleteService as SequenciaDeleteService


class DeleteService:

    def execute(self, profissao_schema: GTbProfissaoIdSchema):

        # Instanciamento da ação
        delete_action = GTbProfissaoDeleteAction()

        # Executa a ação em questão
        data = delete_action.execute(profissao_schema)

        # Validação de Sucesso: Só prossegue se 'data' for verdadeiro
        if data:
            # Instancia o serviço de sequência
            seq_service = SequenciaDeleteService()
            
            # Cria o schema de deleção para a G_SEQUENCIA
            sequencia_schema = GSequenciaDeleteSchema(
                sequencia=profissao_schema.tb_profissao_id,
                tabela='G_TB_PROFISSAO'
            )

            # Executa a atualização da sequência
            seq_service.execute(sequencia_schema)
            
            return data