from packages.v1.administrativo.schemas.t_servico_tipo_schema import TServicoTipoIdSchema # Importação do Schema ajustada
from packages.v1.administrativo.actions.t_servico_tipo.t_servico_tipo_delete_action import DeleteAction # Importação da Action ajustada
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaDeleteSchema
from packages.v1.sequencia.services.g_sequencia.delete_service import DeleteService as SequenciaDeleteService
from fastapi import HTTPException, status


class DeleteService:

    def execute(self, servico_tipo_schema: TServicoTipoIdSchema): # Nome do parâmetro e tipo ajustados

        # Instanciamento da ação
        delete_action = DeleteAction()

        # Executa a ação em questão
        data = delete_action.execute(servico_tipo_schema) # Nome do parâmetro ajustado

        # Validação de Sucesso: Só prossegue se 'data' for verdadeiro
        if data:
            # Instancia o serviço de sequência
            seq_service = SequenciaDeleteService()
            
            # Cria o schema de deleção para a G_SEQUENCIA
            sequencia_schema = GSequenciaDeleteSchema(
                sequencia=servico_tipo_schema.servico_tipo_id,
                tabela='T_SERVICO_TIPO'
            )

            # Executa a atualização da sequência
            seq_service.execute(sequencia_schema)
            
            return data
        
        # Caso a exclusão não tenha afetado nenhuma linha (id não existia, por exemplo)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Não foi possível excluir o registro ou ele não existe."
        )           