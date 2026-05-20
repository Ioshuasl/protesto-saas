from packages.v1.administrativo.actions.t_ato_partetipo.t_ato_partetipo_delete_action import (
    TAtoParteTipoDeleteAction,
)
from packages.v1.administrativo.schemas.t_ato_partetipo_schema import (
    TAtoParteTipoIdSchema,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import DeleteService as SequenciaDeleteService
from fastapi import HTTPException, status


class TAtoParteTipoDeleteService:
   
    def execute(self, t_ato_partetipo_id_schema: TAtoParteTipoIdSchema):
        
        # Instanciamento da ação
        t_ato_partetipo_delete_action = TAtoParteTipoDeleteAction()

        # Executa a ação em questão
        data = t_ato_partetipo_delete_action.execute(t_ato_partetipo_id_schema)

        # Validação de Sucesso: Só prossegue se 'data' for verdadeiro
        if data:
            # Instancia o serviço de sequência
            seq_service = SequenciaDeleteService()
            
            # Cria o schema de deleção para a G_SEQUENCIA
            sequencia_schema = GSequenciaDeleteSchema(
                sequencia=t_ato_partetipo_id_schema.ato_partetipo_id,
                tabela='G_TB_ATO_PARTETIPO'
            )

            # Executa a atualização da sequência
            seq_service.execute(sequencia_schema)
            
            return data
        
        # Caso a exclusão não tenha afetado nenhuma linha (id não existia, por exemplo)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Não foi possível excluir o registro ou ele não existe."
        )        
