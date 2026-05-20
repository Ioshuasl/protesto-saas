from packages.v1.administrativo.actions.g_emolumento.g_emolumento_delete_action import (
    GEmolumentoDeleteAction,
)
from packages.v1.administrativo.schemas.g_emolumento_schema import GEmolumentoIdSchema
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import DeleteService as SequenciaDeleteService


class GEmolumentoDeleteService:

    def execute(self, g_emolumento_id_schema: GEmolumentoIdSchema):

        # Instanciamento da ação
        g_emolumento_delete_action = GEmolumentoDeleteAction()

        # Execução da ação
        data = g_emolumento_delete_action.execute(g_emolumento_id_schema)

        # Validação de Sucesso: Só prossegue se 'data' for verdadeiro
        if data:
            # Instancia o serviço de sequência
            seq_service = SequenciaDeleteService()
            
            # Cria o schema de deleção para a G_SEQUENCIA
            sequencia_schema = GSequenciaDeleteSchema(
                sequencia=g_emolumento_id_schema.emolumento_id,
                tabela='G_EMOLUMENTO'
            )

            # Executa a atualização da sequência
            seq_service.execute(sequencia_schema)
            
            return data
