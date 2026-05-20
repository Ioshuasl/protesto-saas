from packages.v1.administrativo.actions.t_pessoa_representante.t_pessoa_representante_index_action import (
    TPessoaRepresentanteIndexAction,
)
from packages.v1.administrativo.schemas.t_pessoa_representante_schema import (
    TPessoaRepresentantePessoaIdSchema,
)


class TPessoaRepresentanteIndexService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de registros na tabela g_tb_regimebens.
    """

    def execute(
        self,
        t_pessoa_representante_pessoa_id_schema: TPessoaRepresentantePessoaIdSchema,
    ):
        """
        Executa a operação de busca de todos os registros no banco de dados.

        Returns:
            A lista de registros encontrados.
        """
        # Instanciamento da ação
        t_pessoa_representante_index_action = TPessoaRepresentanteIndexAction()

        # Executa a busca de todas as ações
        data = t_pessoa_representante_index_action.execute(
            t_pessoa_representante_pessoa_id_schema
        )

        # Retorna as informações localizadas
        return data
