from fastapi import HTTPException, status
from packages.v1.administrativo.actions.g_cidade.g_cidade_index_action import (
    IndexAction,
)
from packages.v1.administrativo.schemas.g_cidade_schema import GCidadeIndexSchema


class IndexService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de registros na tabela G_CIDADE.
    """

    def execute(self, data: GCidadeIndexSchema):
        """
        Executa a operação de busca de todos os registros no banco de dados.

        Returns:
            A lista de registros encontrados.
        """
        # Instanciamento da ação
        index_action = IndexAction()

        # Executa a busca de todas as ações
        data = index_action.execute(data)

        # Verifica se foram localizados registros
        if not data:
            # Retorna uma exceção
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar os registros de CIDADE",
            )

        # Retorna as informações localizadas
        return data
