from abstracts.action import BaseAction
from packages.v1.servicos.atos.repositories.t_ato_tipo.t_ato_tipo_index_repository import (
    TAtoTipoIndexRepository,
)


class TAtoTipoIndexAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de todos os registros na tabela G_NATUREZA_TITULO.
    """

    def execute(self):
        """
        Executa a operação de listagem no banco de dados.

        Args:
            t_ato_tipo_index_schema (TAtoTipoIndexSchema):
                Esquema contendo parâmetros opcionais de filtro.

        Returns:
            A lista de registros encontrados.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        t_ato_tipo_index_repository = TAtoTipoIndexRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = t_ato_tipo_index_repository.execute()

        # ----------------------------------------------------
        # Retorno da informação
        # --------------------------------
        return response
