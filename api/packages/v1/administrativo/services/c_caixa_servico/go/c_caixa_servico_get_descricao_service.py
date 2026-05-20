from fastapi import HTTPException, status

from packages.v1.administrativo.schemas.c_caixa_servico_schema import CCaixaServicoDescricaoSchema
from packages.v1.administrativo.actions.c_caixa_servico.c_caixa_servico_get_by_descricao_action import ShowAction

class GetDescricaoService:

    def execute(self, caixa_servico_schema: CCaixaServicoDescricaoSchema, messageValidate: bool):

        # Instânciamento de ação
        show_action = ShowAction()

        # Executa a ação em questão
        data = show_action.execute(caixa_servico_schema)

        if messageValidate:
            
            if not data:
                # Retorna uma exceção
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail='Não foi possível localizar o registro'
                )

        # Retorno da informação
        return data