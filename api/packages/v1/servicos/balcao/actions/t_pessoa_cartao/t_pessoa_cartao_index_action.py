from abstracts.action import BaseAction
from packages.v1.servicos.balcao.repositories.t_pessoa_cartao.t_pessoa_cartao_index_repository import (
    TPessoaCartaoIndexRepository,
)
from packages.v1.servicos.balcao.schemas.t_pessoa_cartao_schema import (
    TPessoaCartaoIndexchema,
)


class TPessoaCartaoIndexAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de todos os registros na tabela G_NATUREZA_TITULO.
    """

    def execute(self, t_pessoa_cartao_index_schema: TPessoaCartaoIndexchema):
        """
        Executa a operação de listagem no banco de dados.

        Args:
            t_pessoa_cartao_index_schema (TPessoaCartaoIndexSchema):
                Esquema contendo parâmetros opcionais de filtro.

        Returns:
            A lista de registros encontrados.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        t_pessoa_cartao_index_repository = TPessoaCartaoIndexRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = t_pessoa_cartao_index_repository.execute(
            t_pessoa_cartao_index_schema
        )

        # ----------------------------------------------------
        # Retorno da informação
        # --------------------------------
        return response
