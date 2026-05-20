from fastapi import HTTPException, status
from packages.v1.administrativo.actions.c_caixa_servico.c_caixa_servico_index_action import IndexAction

class IndexService:

    def execute(self):

        # Instânciamento de acções
        index_action = IndexAction()

        # Executa a busca de todas as ações
        data = index_action.execute()

        # Verifica se foi loalizado registros
        if not data:
            # Retorna uma exeção
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Não foi possível localizar os usuários'
            )
        
        # Retorna as informações localizadas
        return data