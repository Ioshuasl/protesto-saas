from packages.v1.administrativo.actions.t_biometria_pessoa.t_biometria_pessoa_delete_action import (
    TBiometriaPessoaDeleteAction,
)
from packages.v1.administrativo.schemas.t_biometria_pessoa_schema import (
    TBiometriaPessoaIdSchema,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import DeleteService as SequenciaDeleteService
from fastapi import HTTPException, status

class TBiometriaPessoaDeleteService:

    def execute(self, t_biometria_pessoa_id_schema: TBiometriaPessoaIdSchema):
        
        
        # Instanciamento da ação       
        t_biometria_pessoa_delete_action = TBiometriaPessoaDeleteAction()
        
        # Execução da ação        
        data = t_biometria_pessoa_delete_action.execute(t_biometria_pessoa_id_schema)

        # Validação de Sucesso: Só prossegue se 'data' for verdadeiro
        if data:
            # Instancia o serviço de sequência
            seq_service = SequenciaDeleteService()
            
            # Cria o schema de deleção para a G_SEQUENCIA
            sequencia_schema = GSequenciaDeleteSchema(
                sequencia=t_biometria_pessoa_id_schema.biometria_pessoa_id,
                tabela='T_BIOMETRIA_PESSOA'
            )

            # Executa a atualização da sequência
            seq_service.execute(sequencia_schema)
            
            return data
        
        # Caso a exclusão não tenha afetado nenhuma linha (id não existia, por exemplo)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Não foi possível excluir o registro ou ele não existe."
        )          
