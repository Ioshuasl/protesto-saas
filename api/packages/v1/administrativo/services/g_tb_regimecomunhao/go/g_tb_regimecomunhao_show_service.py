from fastapi import HTTPException, status
from packages.v1.administrativo.schemas.g_tb_regimecomunhao_schema import GTbRegimecomunhaoIdSchema
from packages.v1.administrativo.actions.g_tb_regimecomunhao.g_tb_regimecomunhao_show_action import ShowAction

class ShowService:

    def execute(self, regimecomunhao_schema: GTbRegimecomunhaoIdSchema):

        # Instanciamento de ação
        show_action = ShowAction()

        # Executa a ação em questão
        data = show_action.execute(regimecomunhao_schema)

        if not data:
            # Retorna uma exceção
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Não foi possível localizar o registro'
            )

        # Retorno da informação
        return data