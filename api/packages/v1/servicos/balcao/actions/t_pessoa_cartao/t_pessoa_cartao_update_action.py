from abstracts.action import BaseAction
from packages.v1.servicos.balcao.repositories.t_pessoa_cartao.t_pessoa_cartao_update_repository import (
    TPessoaCartaoUpdateRepository,
)
from packages.v1.servicos.balcao.schemas.t_pessoa_cartao_schema import (
    TPessoaCartaoUpdateSchema,
)


class TPessoaCartaoUpdateAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a atualização
    de um registro na tabela G_NATUREZA_TITULO.
    """

    def execute(self, data: TPessoaCartaoUpdateSchema):
        """
        Executa a operação de atualização.

        Args:
            data (TPessoaCartaoUpdateSchema):
                O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório de atualização
        # ----------------------------------------------------
        update_repository = TPessoaCartaoUpdateRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = update_repository.execute(data)

        # ----------------------------------------------------
        # Retorno do resultado
        # ----------------------------------------------------
        return response
