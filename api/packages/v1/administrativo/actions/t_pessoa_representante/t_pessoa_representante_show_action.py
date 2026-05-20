from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_pessoa_representante.t_pessoa_representante_delete_repository import (
    TPessoaRepresentanteIdSchema,
)
from packages.v1.administrativo.repositories.t_pessoa_representante.t_pessoa_representante_show_repository import (
    TPessoaRepresentanteShowRepository,
)


class TPessoaRepresentanteShowAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a exibição
    de um registro na tabela g_tb_regimebens.
    """

    def execute(self, t_pessoa_representante_id_schema: TPessoaRepresentanteIdSchema):
        """
        Executa a operação de exibição.

        Args:
            regimebens_schema (GTbRegimebensIdSchema): O esquema com o ID do registro a ser exibido.

        Returns:
            O resultado da operação de exibição.
        """
        # Instânciamento do repositório
        t_pessoa_representante_show_repository = TPessoaRepresentanteShowRepository()

        # Execução do repositório
        response = t_pessoa_representante_show_repository.execute(
            t_pessoa_representante_id_schema
        )

        # Retorno da informação
        return response
