from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_emolumento_item.g_emolumento_item_index_repository import (
    GEmolumentoItemIndexRepository,
)
from packages.v1.administrativo.schemas.g_emolumento_item_schema import (
    GEmolumentoItemByTipoAtoSchema,
)


class GEmolumentoItemIndexAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de todos os registros na tabela G_NATUREZA_TITULO.
    """

    def execute(self, data: GEmolumentoItemByTipoAtoSchema):
        """
        Executa a operação de listagem no banco de dados.

        Args:
            g_emolumento_item_index_schema (GEmolumentoItemIndexSchema):
                Esquema contendo parâmetros opcionais de filtro.

        Returns:
            A lista de registros encontrados.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        repository = GEmolumentoItemIndexRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = repository.execute(data)

        # ----------------------------------------------------
        # Retorno da informação
        # --------------------------------
        return response
