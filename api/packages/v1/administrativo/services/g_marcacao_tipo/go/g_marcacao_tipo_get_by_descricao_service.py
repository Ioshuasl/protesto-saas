from fastapi import HTTPException, status
from packages.v1.administrativo.actions.g_marcacao_tipo.g_marcacao_tipo_get_by_descricao_action import (
    GMarcacaoTipoGetByDescricaoAction,
)
from packages.v1.administrativo.schemas.g_marcacao_tipo_schema import (
    GMarcacaoTipoDescricaoSchema,
)


class GMarcacaoTipoGetByDescricaoService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela G_MARCACAO_TIPO pela sua descrição.
    """

    def execute(self, data: GMarcacaoTipoDescricaoSchema, messageValidate: bool):
        # Instanciamento da ação
        show_action = GMarcacaoTipoGetByDescricaoAction()

        # Executa a ação em questão
        data = show_action.execute(data)

        if messageValidate:

            if not data:
                # Retorna uma exceção
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Não foi possível localizar o registro de G_MARCACAO_TIPO",
                )

        # Retorno da informação
        return data
