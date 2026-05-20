from packages.v1.administrativo.actions.t_pessoa_representante.t_pessoa_representante_update_action import (
    TPessoaRepresentanteUpdateAction,
)
from packages.v1.administrativo.repositories.t_pessoa_representante.t_pessoa_representante_update_repository import (
    TPessoaRepresentanteUpdateSchema,
)


class TPessoaRepresentanteUpdateService:
    """
    Serviço para a operação de atualização de um registro na tabela
    g_tb_regimebens.
    """

    def execute(
        self, t_pessoa_representante_update_schema: TPessoaRepresentanteUpdateSchema
    ):
        """
        Executa a operação de atualização no banco de dados.

        Args:
            regimebens_schema (GTbRegimebensUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # Instanciamento de ações
        t_pessoa_representante_update_action = TPessoaRepresentanteUpdateAction()

        # Retorna o resultado da operação
        return t_pessoa_representante_update_action.execute(
            t_pessoa_representante_update_schema
        )
