from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.g_cartorio.g_cartorio_index_repository import (
    GCartorioIndexRepository,
)


class GCartorioIndexAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de todos os registros na tabela G_NATUREZA_TITULO.
    """

    def execute(self):
        """
        Executa a operação de listagem no banco de dados.

        Args:
            g_cartorio_index_schema (GCartorioIndexSchema):
                Esquema contendo parâmetros opcionais de filtro.

        Returns:
            A lista de registros encontrados.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        g_cartorio_index_repository = GCartorioIndexRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = g_cartorio_index_repository.execute()

        # ----------------------------------------------------
        # Retorno da informação
        # --------------------------------
        return response
