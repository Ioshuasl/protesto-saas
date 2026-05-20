from fastapi import HTTPException, status
from packages.v1.administrativo.schemas.g_medida_tipo_schema import GMedidaTipoIdSchema
from packages.v1.administrativo.actions.g_medida_tipo.g_medida_tipo_show_action import ShowAction

class ShowService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela g_medida_tipo.
    """

    def execute(self, medida_tipo_schema: GMedidaTipoIdSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            medida_tipo_schema (GMedidaTipoIdSchema): O esquema com o ID a ser buscado.

        Returns:
            O resultado da busca.
        """
        # Instanciamento da ação
        show_action = ShowAction()

        # Executa a ação em questão
        data = show_action.execute(medida_tipo_schema)

        if not data:
            # Retorna uma exceção
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Não foi possível localizar o registro de G_MEDIDA_TIPO'
            )

        # Retorno da informação
        return data