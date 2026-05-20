from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_biometria_pessoa.t_biometria_pessoa_show_repository import (
    TBiometriaPessoaShowRepository,
)
from packages.v1.administrativo.schemas.t_biometria_pessoa_schema import (
    TBiometriaPessoaIdSchema,
)


class TBiometriaPessoaShowAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a exibição
    de um registro na tabela G_NATUREZA_TITULO.
    """

    def execute(self, t_biometria_pessoa_id_schema: TBiometriaPessoaIdSchema):
        """
        Executa a operação de exibição.

        Args:
            t_biometria_pessoa_id_schema (TBiometriaPessoaIdSchema):
                O esquema com o ID do registro a ser exibido.

        Returns:
            O resultado da operação de exibição.
        """
        # ----------------------------------------------------
        # Instanciamento do repositório
        # ----------------------------------------------------
        t_biometria_pessoa_show_repository = TBiometriaPessoaShowRepository()

        # ----------------------------------------------------
        # Execução do repositório
        # ----------------------------------------------------
        response = t_biometria_pessoa_show_repository.execute(
            t_biometria_pessoa_id_schema
        )

        # ----------------------------------------------------
        # Retorno da informação
        # ----------------------------------------------------
        return response
