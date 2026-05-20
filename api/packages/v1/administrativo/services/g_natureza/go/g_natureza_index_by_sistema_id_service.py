from fastapi import HTTPException, status
from packages.v1.administrativo.actions.g_natureza.g_natureza_index_by_sistema_id_action import (
    IndexActionBySistemaId,
)
from packages.v1.administrativo.schemas.g_natureza_schema import (
    GNaturezaSistemaIdSchema,
)


class IndexBySistemaIdService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de registros na tabela g_natureza.
    """

    def execute(self, g_natureza_sistema_id_schema: GNaturezaSistemaIdSchema):
        """
        Executa a operação de busca de todos os registros no banco de dados.

        Returns:
            A lista de registros encontrados.
        """
        # Instanciamento da ação
        index_action = IndexActionBySistemaId()

        # Executa a busca de todas as ações
        data = index_action.execute(g_natureza_sistema_id_schema)

        # Verifica se foram localizados registros
        if not data:
            # Retorna uma exceção
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar os registros de Natureza",
            )

        # Retorna as informações localizadas
        return data
