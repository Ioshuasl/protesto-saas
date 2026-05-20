from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_biometria_pessoa.t_biometria_pessoa_index_repository import (
    TBiometriaPessoaIndexRepository,
)
from packages.v1.administrativo.schemas.t_biometria_pessoa_schema import (
    TBiometriaPessoaIndexSchema,
)


class TBiometriaPessoaIndexAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de todos os registros na tabela G_NATUREZA_TITULO.
    """

    def execute(self, biometria_pessoa_index_schema: TBiometriaPessoaIndexSchema):
        """
        Executa a operação de listagem no banco de dados.

        Args:
            t_biometria_pessoa_index_schema (TBiometriaPessoaIndexSchema):
                Esquema contendo parâmetros opcionais de filtro.

        Returns:
            A lista de registros encontrados.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        t_biometria_pessoa_index_repository = TBiometriaPessoaIndexRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = t_biometria_pessoa_index_repository.execute(
            biometria_pessoa_index_schema
        )

        # ----------------------------------------------------
        # Retorno da informação
        # --------------------------------
        return response
