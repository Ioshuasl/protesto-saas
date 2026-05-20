from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.t_pessoa_schema import TPessoaNameSchema


class TPessoaGetByNameAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela g_tb_regimebens por descrição.
    """

    def execute(self, t_pessoa_name_schema: TPessoaNameSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            regimebens_schema (GTbRegimebensDescricaoSchema): O esquema com a descrição a ser buscada.

        Returns:
            O registro encontrado ou None.
        """
        # Instanciamento do repositório
        t_pessoa_get_by_name = TPessoaGetByNameAction()

        # Execução do repositório
        response = t_pessoa_get_by_name.execute(t_pessoa_name_schema)

        # Retorno da informação
        return response
