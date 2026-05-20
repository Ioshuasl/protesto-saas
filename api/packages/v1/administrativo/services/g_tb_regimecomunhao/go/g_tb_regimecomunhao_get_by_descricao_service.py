from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.g_tb_regimecomunhao_schema import GTbRegimecomunhaoDescricaoSchema
from packages.v1.administrativo.actions.g_tb_regimecomunhao.g_tb_regimecomunhao_get_by_descricao_action import GetByDescricaoAction

class GetByDescricaoService:

    def execute(self, regimecomunhao_schema: GTbRegimecomunhaoDescricaoSchema, messageValidate: bool):
        """
        Executa a lógica de negócio para a exibição de um registro na tabela
        g_tb_regimecomunhao pela descrição.
        """
        # Instanciamento de ação
        show_action = GetByDescricaoAction()

        # Executa a ação em questão
        data = show_action.execute(regimecomunhao_schema)

        if messageValidate:
            
            if not data:
                # Retorna uma exceção
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Não foi possível localizar o registro'
                )

        # Retorno da informação
        return data