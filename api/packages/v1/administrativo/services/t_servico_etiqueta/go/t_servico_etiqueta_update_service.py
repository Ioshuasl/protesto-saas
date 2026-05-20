from packages.v1.administrativo.schemas.t_servico_etiqueta_schema import TServicoEtiquetaUpdateSchema # Importação do Schema ajustada
from packages.v1.administrativo.actions.t_servico_etiqueta.t_servico_etiqueta_update_action import UpdateAction # Importação da Action ajustada

class UpdateService:
    """
    Serviço para a operação de atualização de um registro na tabela
    T_SERVICO_ETIQUETA.
    """
    def execute(self, servico_etiqueta_id : int, servico_etiqueta_schema: TServicoEtiquetaUpdateSchema): # Nomes dos parâmetros ajustados
        """
        Executa a operação de atualização no banco de dados.

        Args:
            servico_etiqueta_id (int): O ID do registro a ser atualizado (SERVICO_ETIQUETA_ID).
            servico_etiqueta_schema (TServicoEtiquetaUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # Instanciamento de ações
        update_action = UpdateAction()

        # Retorna o resultado da operação
        return update_action.execute(servico_etiqueta_id, servico_etiqueta_schema) # Parâmetros ajustados