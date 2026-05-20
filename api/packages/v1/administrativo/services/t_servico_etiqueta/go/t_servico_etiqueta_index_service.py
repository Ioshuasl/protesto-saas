from fastapi import HTTPException, status
# Importação da Action ajustada para o novo prefixo
from packages.v1.administrativo.actions.t_servico_etiqueta.t_servico_etiqueta_index_action import IndexAction

class IndexService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de registros na tabela T_SERVICO_ETIQUETA.
    """

    def execute(self):
        """
        Executa a operação de busca de todos os registros no banco de dados.

        Returns:
            A lista de registros encontrados.
        """
        # Instanciamento da ação
        index_action = IndexAction()

        # Executa a busca de todas as ações
        data = index_action.execute()

        # Verifica se foram localizados registros
        if not data:
            # Retorna uma exceção
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Não foi possível localizar os registros de T_SERVICO_ETIQUETA'
            )
        
        # Retorna as informações localizadas
        return data