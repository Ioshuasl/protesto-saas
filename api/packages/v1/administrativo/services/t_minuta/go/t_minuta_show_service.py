from fastapi import HTTPException, status
from packages.v1.administrativo.schemas.t_minuta_schema import TMinutaIdSchema
from packages.v1.administrativo.actions.t_minuta.t_minuta_show_action import ShowAction

class ShowService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela t_minuta.
    """

    def execute(self, minuta_schema: TMinutaIdSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            minuta_schema (TMinutaIdSchema): O esquema com o ID a ser buscado.

        Returns:
            O resultado da busca.
        """
        # Instanciamento da ação
        show_action = ShowAction()

        # Executa a ação em questão
        data = show_action.execute(minuta_schema)

        if not data:
            # Retorna uma exceção
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Não foi possível localizar o registro de MINUTA'
            )

        # Retorno da informação
        return data