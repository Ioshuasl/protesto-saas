from fastapi import HTTPException, status
from packages.v1.administrativo.actions.g_tb_regimecomunhao.g_tb_regimecomunhao_index_action import IndexAction

class IndexService:

    def execute(self):
        """
        Executa a lógica de negócio para a listagem de todos os registros na tabela
        g_tb_regimecomunhao.
        """
        # Instanciamento de ações
        index_action = IndexAction()

        # Executa a busca de todas as ações
        data = index_action.execute()

        # Verifica se foi localizado registros
        if not data:
            # Retorna uma exceção
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Não foi possível localizar os regimes de comunhão'
            )
        
        # Retorna as informações localizadas
        return data