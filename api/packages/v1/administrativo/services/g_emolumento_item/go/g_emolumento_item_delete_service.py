from packages.v1.administrativo.actions.g_emolumento_item.g_emolumento_item_delete_action import (
    GEmolumentoItemDeleteAction,
)
from packages.v1.administrativo.schemas.g_emolumento_item_schema import (
    GEmolumentoItemIdSchema,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import DeleteService as SequenciaDeleteService


class GEmolumentoItemDeleteService:

    def execute(self, g_emolumento_item_id_schema: GEmolumentoItemIdSchema):

        # Instanciamento da ação
        g_emolumento_item_delete_action = GEmolumentoItemDeleteAction()

        # Execução da ação
        data = g_emolumento_item_delete_action.execute(g_emolumento_item_id_schema)

        # Validação de Sucesso: Só prossegue se 'data' for verdadeiro
        if data:
            # Instancia o serviço de sequência
            seq_service = SequenciaDeleteService()

            # Cria o schema de deleção para a G_SEQUENCIA
            sequencia_schema = GSequenciaDeleteSchema(
                sequencia=g_emolumento_item_id_schema.emolumento_item_id,
                tabela='G_EMOLUMENTO'
            )

            # Executa a atualização da sequência
            seq_service.execute(sequencia_schema)

            return data

        # Caso a exclusão não tenha afetado nenhuma linha (id não existia, por exemplo)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Não foi possível excluir o registro ou ele não existe.",
        )

