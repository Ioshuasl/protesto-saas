from packages.v1.administrativo.actions.t_censec_qualidadeato.t_censec_qualidadeato_delete_action import (
    TCensecQualidadeAtoDeleteAction,
)
from packages.v1.administrativo.schemas.t_censec_qualidadeato_schema import (
    TCensecQualidadeAtoIdSchema,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import DeleteService as SequenciaDeleteService
from fastapi import HTTPException, status


class TCensecQualidadeAtoDeleteService:
    
    def execute(self, t_censec_qualidade_ato_id_schema: TCensecQualidadeAtoIdSchema):
        
        # Instanciamento da ação responsável pela exclusão        
        t_censec_qualidade_ato_delete_action = TCensecQualidadeAtoDeleteAction()
        
        # Execução da ação e obtenção do resultado        
        data = t_censec_qualidade_ato_delete_action.execute(
            t_censec_qualidade_ato_id_schema
        )

        # Validação de Sucesso: Só prossegue se 'data' for verdadeiro
        if data:
            # Instancia o serviço de sequência
            seq_service = SequenciaDeleteService()
            
            # Cria o schema de deleção para a G_SEQUENCIA
            sequencia_schema = GSequenciaDeleteSchema(
                sequencia=t_censec_qualidade_ato_id_schema.censec_qualidadeato_id,
                tabela='T_CENSEC_QUALIDADEATO'
            )

            # Executa a atualização da sequência
            seq_service.execute(sequencia_schema)
            
            return data
        
        # Caso a exclusão não tenha afetado nenhuma linha (id não existia, por exemplo)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Não foi possível excluir o registro ou ele não existe."
        )         
