from packages.v1.administrativo.actions.t_imovel.t_imovel_delete_action import (
    TImovelDeleteAction,
)
from packages.v1.administrativo.schemas.t_imovel_schema import TImovelIdSchema
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import DeleteService as SequenciaDeleteService
from fastapi import HTTPException, status


class TImovelDeleteService:
    
    def execute(self, t_imovel_id_schema: TImovelIdSchema):
        
        # Instanciamento da ação
        t_imovel_delete_action = TImovelDeleteAction()

        # Executa a ação em questão
        data = t_imovel_delete_action.execute(t_imovel_id_schema)

        # Validação de Sucesso: Só prossegue se 'data' for verdadeiro
        if data:
            # Instancia o serviço de sequência
            seq_service = SequenciaDeleteService()
            
            # Cria o schema de deleção para a G_SEQUENCIA
            sequencia_schema = GSequenciaDeleteSchema(
                sequencia=t_imovel_id_schema.imovel_id,
                tabela='T_IMOVEL'
            )

            # Executa a atualização da sequência
            seq_service.execute(sequencia_schema)
            
            return data
        
        # Caso a exclusão não tenha afetado nenhuma linha (id não existia, por exemplo)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Não foi possível excluir o registro ou ele não existe."
        )         
