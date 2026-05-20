from packages.v1.administrativo.schemas.t_censec_naturezalitigio_schema import TCensecNaturezalitigioIdSchema
from packages.v1.administrativo.actions.t_censec_naturezalitigio.t_censec_naturezalitigio_delete_action import DeleteAction
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import DeleteService as SequenciaDeleteService
from fastapi import HTTPException, status

class DeleteService:
    
    def execute(self, censec_naturezalitigio_schema: TCensecNaturezalitigioIdSchema):
        
        # Instanciamento da ação
        delete_action = DeleteAction()

        # Executa a ação em questão
        data = delete_action.execute(censec_naturezalitigio_schema)

        # Validação de Sucesso: Só prossegue se 'data' for verdadeiro
        if data:
            # Instancia o serviço de sequência
            seq_service = SequenciaDeleteService()
            
            # Cria o schema de deleção para a G_SEQUENCIA
            sequencia_schema = GSequenciaDeleteSchema(
                sequencia=censec_naturezalitigio_schema.censec_naturezalitigio_id,
                tabela='T_CENSEC_NATUREZALITIGIO'
            )

            # Executa a atualização da sequência
            seq_service.execute(sequencia_schema)
            
            return data
        
        # Caso a exclusão não tenha afetado nenhuma linha (id não existia, por exemplo)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Não foi possível excluir o registro ou ele não existe."
        )        