from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_censec_qualidadeato.t_censec_qualidadeato_index_repository import (
    TCensecQualidadeAtoIndexRepository,
)
from packages.v1.administrativo.schemas.t_censec_qualidadeato_schema import (
    TCensecQualidadeAtoIndexSchema,
)


class TCensecQualidadeAtoIndexAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de todos os registros na tabela T_CENSEC_QUALIDADEATO.
    """

    def execute(
        self, censec_qualidade_ato_index_schema: TCensecQualidadeAtoIndexSchema
    ):
        """
        Executa a operação de listagem no banco de dados.

        Returns:
            A lista de registros encontrados.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        t_censec_qualidadeato_index_repository = TCensecQualidadeAtoIndexRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = t_censec_qualidadeato_index_repository.execute(
            censec_qualidade_ato_index_schema
        )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return response
