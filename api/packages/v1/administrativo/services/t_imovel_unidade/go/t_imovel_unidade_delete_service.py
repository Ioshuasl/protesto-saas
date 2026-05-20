from packages.v1.administrativo.actions.t_imovel_unidade.t_imovel_unidade_delete_action import (
    TImovelUnidadeDeleteAction,
)
from packages.v1.administrativo.schemas.t_imovel_unidade_schema import (
    TImovelUnidadeIdSchema,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import DeleteService as SequenciaDeleteService
from fastapi import HTTPException, status


class TImovelUnidadeDeleteService:
    
    def execute(self, t_imovel_unidade_id_schema: TImovelUnidadeIdSchema):
        
        # Instanciamento da ação
        t_imovel_unidade_delete = TImovelUnidadeDeleteAction()

        # Executa a ação em questão
        data = t_imovel_unidade_delete.execute(t_imovel_unidade_id_schema)

        # Validação de Sucesso: Só prossegue se 'data' for verdadeiro
        if data:
            # Instancia o serviço de sequência
            seq_service = SequenciaDeleteService()
            
            # Cria o schema de deleção para a G_SEQUENCIA
            sequencia_schema = GSequenciaDeleteSchema(
                sequencia=t_imovel_unidade_id_schema.imovel_unidade_id,
                tabela='T_IMOVEL_UNIDADE'
            )

            # Executa a atualização da sequência
            seq_service.execute(sequencia_schema)
            
            return data
        
        # Caso a exclusão não tenha afetado nenhuma linha (id não existia, por exemplo)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Não foi possível excluir o registro ou ele não existe."
        )          
