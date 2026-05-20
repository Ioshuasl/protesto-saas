from packages.v1.administrativo.actions.t_pessoa_representante.t_pessoa_representante_delete_action import (
    TPessoaRepresentanteDeleteAction,
)
from packages.v1.administrativo.schemas.t_pessoa_representante_schema import (
    TPessoaRepresentanteIdSchema,
)
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import DeleteService as SequenciaDeleteService
from fastapi import HTTPException, status


class TPessoaRepresentanteDeleteService:

    def execute(self, t_pessoa_representante_id_schema: TPessoaRepresentanteIdSchema):

        # Instanciamento da ação
        t_pessoa_representante_delete_action = TPessoaRepresentanteDeleteAction()

        # Executa a ação em questão
        data = t_pessoa_representante_delete_action.execute(
            t_pessoa_representante_id_schema
        )

        # Validação de Sucesso: Só prossegue se 'data' for verdadeiro
        if data:
            # Instancia o serviço de sequência
            seq_service = SequenciaDeleteService()
            
            # Cria o schema de deleção para a G_SEQUENCIA
            sequencia_schema = GSequenciaDeleteSchema(
                sequencia=t_pessoa_representante_id_schema.pessoa_representante_id,
                tabela='T_PESSOA_REPRESENTANTE'
            )

            # Executa a atualização da sequência
            seq_service.execute(sequencia_schema)
            
            return data
        
        # Caso a exclusão não tenha afetado nenhuma linha (id não existia, por exemplo)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Não foi possível excluir o registro ou ele não existe."
        )          
