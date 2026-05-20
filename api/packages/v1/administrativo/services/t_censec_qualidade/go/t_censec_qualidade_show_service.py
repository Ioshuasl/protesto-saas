from fastapi import HTTPException, status
from packages.v1.administrativo.schemas.t_censec_qualidade_schema import TCensecQualidadeIdSchema
from packages.v1.administrativo.actions.t_censec_qualidade.t_censec_qualidade_show_action import ShowAction

class ShowService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela t_censec_qualidade.
    """

    def execute(self, censec_qualidade_schema: TCensecQualidadeIdSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            censec_qualidade_schema (TCensecQualidadeIdSchema): O esquema com o ID a ser buscado.

        Returns:
            O resultado da busca.
        """
        # Instanciamento da ação
        show_action = ShowAction()

        # Executa a ação em questão
        data = show_action.execute(censec_qualidade_schema)

        if not data:
            # Retorna uma exceção
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Não foi possível localizar o registro de CENSEC_QUALIDADE'
            )

        # Retorno da informação
        return data