from abstracts.action import BaseAction
from packages.v1.administrativo.schemas.t_tb_reconhecimentotipo_schema import TTbReconhecimentotipoDescricaoSchema
from packages.v1.administrativo.repositories.t_tb_reconhecimentotipo.t_tb_reconhecimentotipo_get_by_descricao_repository import GetByDescricaoRepository

class GetByDescricaoAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela t_tb_reconhecimentotipo por descrição.
    """

    def execute(self, reconhecimentotipo_schema: TTbReconhecimentotipoDescricaoSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            reconhecimentotipo_schema (T_TbReconhecimentotipoDescricaoSchema): O esquema com a descrição a ser buscada.

        Returns:
            O registro encontrado ou None.
        """
        # Instanciamento do repositório
        show_repository = GetByDescricaoRepository()

        # Execução do repositório
        response = show_repository.execute(reconhecimentotipo_schema)

        # Retorno da informação
        return response
