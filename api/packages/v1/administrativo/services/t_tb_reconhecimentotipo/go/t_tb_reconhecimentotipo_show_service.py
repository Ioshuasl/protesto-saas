from fastapi import HTTPException, status
from packages.v1.administrativo.schemas.t_tb_reconhecimentotipo_schema import TTbReconhecimentotipoIdSchema
from packages.v1.administrativo.actions.t_tb_reconhecimentotipo.t_tb_reconhecimentotipo_show_action import ShowAction

class ShowService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela t_tb_reconhecimentotipo.
    """

    def execute(self, reconhecimentotipo_schema: TTbReconhecimentotipoIdSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            reconhecimentotipo_schema (T_TbReconhecimentotipoIdSchema): O esquema com o ID a ser buscado.

        Returns:
            O resultado da busca.
        """
        # Instanciamento da ação
        show_action = ShowAction()

        # Executa a ação em questão
        data = show_action.execute(reconhecimentotipo_schema)

        if not data:
            # Retorna uma exceção
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Não foi possível localizar o registro de tipo de reconhecimento'
            )

        # Retorno da informação
        return data
