from fastapi import HTTPException, status
from packages.v1.administrativo.schemas.t_censec_schema import TCensecIdSchema
from packages.v1.administrativo.actions.t_censec.t_censec_show_action import ShowAction

class ShowService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela t_censec.
    """

    def execute(self, censec_schema: TCensecIdSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            censec_schema (TCensecIdSchema): O esquema com o ID a ser buscado.

        Returns:
            O resultado da busca.
        """
        # Instanciamento da ação
        show_action = ShowAction()

        # Executa a ação em questão
        data = show_action.execute(censec_schema)

        if not data:
            # Retorna uma exceção
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Não foi possível localizar o registro de CENSEC'
            )

        # Retorno da informação
        return data