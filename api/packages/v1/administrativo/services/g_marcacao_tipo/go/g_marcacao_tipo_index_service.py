from fastapi import HTTPException, status

from packages.v1.administrativo.actions.g_marcacao_tipo.g_marcacao_tipo_index_action import (
    GMarcacaoTipoIndexAction,
)


class GMarcacaoTipoIndexService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de registros na tabela G_MARCACAO_TIPO.
    """

    def execute(self):

        # Instanciamento da ação
        action = GMarcacaoTipoIndexAction()

        # Executa a busca de todas as ações
        data = action.execute()

        # Verifica se foram localizados registros
        if not data:
            # Retorna uma exceção
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar os registros de G_MARCACAO_TIPO",
            )

        # Retorna as informações localizadas
        return data
