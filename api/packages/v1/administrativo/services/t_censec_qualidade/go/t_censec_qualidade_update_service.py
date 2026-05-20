from packages.v1.administrativo.schemas.t_censec_qualidade_schema import TCensecQualidadeUpdateSchema
from packages.v1.administrativo.actions.t_censec_qualidade.t_censec_qualidade_update_action import UpdateAction

class UpdateService:
    """
    Serviço para a operação de atualização de um registro na tabela
    t_censec_qualidade.
    """
    def execute(self, censec_qualidade_id: int, censec_qualidade_schema: TCensecQualidadeUpdateSchema):
        """
        Executa a operação de atualização no banco de dados.

        Args:
            censec_qualidade_schema (TCensecQualidadeUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # Instanciamento de ações
        update_action = UpdateAction()

        # Retorna o resultado da operação
        return update_action.execute(censec_qualidade_id, censec_qualidade_schema)