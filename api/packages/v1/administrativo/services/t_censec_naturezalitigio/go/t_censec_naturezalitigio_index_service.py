from fastapi import HTTPException, status
from packages.v1.administrativo.actions.t_censec_naturezalitigio.t_censec_naturezalitigio_index_action import IndexAction

class IndexService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de registros na tabela t_censec_naturezalitigio.
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
                detail='Não foi possível localizar os registros de CENSEC_NATUREZALITIGIO'
            )
        
        # Retorna as informações localizadas
        return data