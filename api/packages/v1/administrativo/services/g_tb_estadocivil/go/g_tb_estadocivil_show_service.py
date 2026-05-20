from fastapi import HTTPException, status
from packages.v1.administrativo.schemas.g_tb_estadocivil_schema import GTbEstadoCivilIdSchema
from packages.v1.administrativo.actions.g_tb_estadocivil.g_tb_estadocivil_show_action import ShowAction

class ShowService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela G_TB_ESTADOCIVIL.
    """

    def execute(self, estado_civil_schema: GTbEstadoCivilIdSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            estado_civil_schema (GTBEstadoCivilIdSchema): O esquema com o ID a ser buscado.

        Returns:
            O resultado da busca.
        """
        # Instanciamento da ação
        show_action = ShowAction()

        # Executa a ação em questão
        data = show_action.execute(estado_civil_schema)

        if not data:
            # Retorna uma exceção
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Não foi possível localizar o registro de Estado Civil'
            )

        # Retorno da informação
        return data