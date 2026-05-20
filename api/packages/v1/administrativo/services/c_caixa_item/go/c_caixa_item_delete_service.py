from fastapi import HTTPException, status
from packages.v1.administrativo.actions.c_caixa_item.c_caixa_item_delete_action import DeleteAction
from packages.v1.administrativo.actions.c_caixa_item.c_caixa_item_show_action import ShowAction
from packages.v1.administrativo.schemas.c_caixa_item_schema import CaixaItemSchema
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import DeleteService as SequenciaDeleteService


class DeleteService:

    def execute(self, caixa_item_schema: CaixaItemSchema):

        # Instânciamento de classe
        showAction = ShowAction()

        # Obtém o registro desejado
        data = showAction.execute(caixa_item_schema)

        # Verifica se o registro não existe
        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Não foi possível localizar o registro'
            )

        # Instanciamento de ações
        deleteAction = DeleteAction()

        # Retorna todos produtos desejados
        data = deleteAction.execute(caixa_item_schema)

        # Validação de Sucesso: Só prossegue se 'data' for verdadeiro
        if data:
            # Instancia o serviço de sequência
            seq_service = SequenciaDeleteService()
            
            # Cria o schema de deleção para a G_SEQUENCIA
            sequencia_schema = GSequenciaDeleteSchema(
                sequencia=caixa_item_schema.caixa_item_id,
                tabela='C_CAIXA_ITEM'
            )

            # Executa a atualização da sequência
            seq_service.execute(sequencia_schema)
            
            return data        