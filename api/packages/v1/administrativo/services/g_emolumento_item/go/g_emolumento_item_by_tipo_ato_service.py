from packages.v1.administrativo.actions.g_emolumento_item.g_emolumento_item_by_tipo_ato_action import (
    GEmolumentoItemByTipoAtoAction,
)
from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.g_emolumento_item_schema import (
    GEmolumentoItemByTipoAtoSchema,
)


class GEmolumentoItemByTipoAtoService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de registros na tabela G_EMOLUMENTO_ITEM.
    """

    def execute(self, data: GEmolumentoItemByTipoAtoSchema):
        """
        Executa a operação de busca de todos os registros no banco de dados.

        Args:
            g_emolumento_item_index_schema (GEmolumentoItemIndexSchema):
                Esquema que pode conter filtros ou parâmetros de busca.

        Returns:
            A lista de registros encontrados.
        """
        # ----------------------------------------------------
        # Instanciamento da ação
        # ----------------------------------------------------
        action = GEmolumentoItemByTipoAtoAction()

        # ----------------------------------------------------
        # Execução da ação
        # ----------------------------------------------------
        response = action.execute(data)

        # ----------------------------------------------------
        # Verificação de retorno
        # ----------------------------------------------------
        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar registros de G_EMOLUMENTO_ITEM.",
            )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return response
