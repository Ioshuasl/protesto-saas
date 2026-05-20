from packages.v1.administrativo.schemas.c_caixa_servico_schema import CCaixaServicoIdSchema
from packages.v1.administrativo.actions.c_caixa_servico.c_caixa_servico_delete_action import DeleteAction
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import DeleteService as SequenciaDeleteService


class DeleteService:

    def execute(self, caixa_servico_schema: CCaixaServicoIdSchema):

        # Instânciamento de ação
        delete_action = DeleteAction()

        # Executa a ação em questão
        data = delete_action.execute(caixa_servico_schema)

        # Validação de Sucesso: Só prossegue se 'data' for verdadeiro
        if data:
            # Instancia o serviço de sequência
            seq_service = SequenciaDeleteService()
            
            # Cria o schema de deleção para a G_SEQUENCIA
            sequencia_schema = GSequenciaDeleteSchema(
                sequencia=caixa_servico_schema.caixa_servico_id,
                tabela='C_CAIXA_SERVICO'
            )

            # Executa a atualização da sequência
            seq_service.execute(sequencia_schema)
            
            return data
        