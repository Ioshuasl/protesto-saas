from packages.v1.administrativo.schemas.t_servico_tipo_schema import TServicoTipoUpdateSchema # Importação do Schema ajustada
from packages.v1.administrativo.actions.t_servico_tipo.t_servico_tipo_update_action import UpdateAction # Importação da Action ajustada

class UpdateService:
    """
    Serviço para a operação de atualização de um registro na tabela
    T_SERVICO_TIPO. # Nome da tabela ajustado
    """
    def execute(self, servico_tipo_id : int, servico_tipo_schema: TServicoTipoUpdateSchema): # Nomes dos parâmetros ajustados
        """
        Executa a operação de atualização no banco de dados.

        Args:
            servico_tipo_id (int): O ID do registro a ser atualizado (SERVICO_TIPO_ID).
            servico_tipo_schema (TServicoTipoUpdateSchema): O esquema com os dados a serem atualizados. # Nome do tipo ajustado

        Returns:
            O resultado da operação de atualização.
        """
        # Instanciamento de ações
        update_action = UpdateAction()

        # Retorna o resultado da operação
        return update_action.execute(servico_tipo_id, servico_tipo_schema) # Parâmetros ajustados