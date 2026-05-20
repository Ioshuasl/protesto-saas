from packages.v1.administrativo.actions.g_marcacao_tipo.g_marcacao_tipo_delete_action import (
    GMarcacaoTipoDeleteAction,
)
from packages.v1.administrativo.schemas.g_marcacao_tipo_schema import (
    GMarcacaoTipoIdSchema,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import DeleteService


class GMarcacaoTipoDeleteService:

    def execute(self, data: GMarcacaoTipoIdSchema):

        # Instanciamento da ação
        delete_action = GMarcacaoTipoDeleteAction()

        # Executa a ação em questão
        data = delete_action.execute(data)

        # Validação de Sucesso: Só prossegue se 'data' for verdadeiro
        if data:

            # Instancia o serviço de sequência
            sequencia_service = DeleteService()

            # Cria o schema de deleção para a G_SEQUENCIA
            sequencia_schema = GSequenciaDeleteSchema(
                sequencia=data.marcacao_tipo_id,
                tabela="G_MARCACAO_TIPO",
            )

            # Executa a atualização da sequência
            sequencia_service.execute(sequencia_schema)

            return data
