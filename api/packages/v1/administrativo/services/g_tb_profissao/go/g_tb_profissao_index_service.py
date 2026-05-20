from fastapi import HTTPException, status
from packages.v1.administrativo.actions.g_tb_profissao.g_tb_profissao_index_action import GTbProfissaoIndexAction

class IndexService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de registros na tabela G_TB_PROFISSAO.
    """

    def execute(self):
        """
        Executa a operação de busca de todos os registros no banco de dados.

        Returns:
            A lista de registros encontrados.
        """
        # Instanciamento da ação
        index_action = GTbProfissaoIndexAction()

        # Executa a busca de todas as ações
        data = index_action.execute()

        # Verifica se foram localizados registros
        if not data:
            # Retorna uma exceção
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Não foi possível localizar os registros de profissão'
            )
        
        # Retorna as informações localizadas
        return data