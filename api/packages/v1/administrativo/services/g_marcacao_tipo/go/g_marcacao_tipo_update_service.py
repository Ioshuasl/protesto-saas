
from actions.data.base64 import Base64
from packages.v1.administrativo.schemas.g_marcacao_tipo_schema import (
    GMarcacaoTipoUpdateSchema,
)
from packages.v1.administrativo.actions.g_marcacao_tipo.g_marcacao_tipo_update_action import (
    GMarcacaoTipoUpdateAction,
)


class GMarcacaoTipoUpdateService:
    """
    Serviço para a operação de atualização de um registro na tabela
    G_MARCACAO_TIPO.
    """

    def execute(self, data: GMarcacaoTipoUpdateSchema):

        if getattr(data, "texto", None):

            texto = data.texto
            if isinstance(texto, str):
                if ".docx" in texto.lower():
                    if hasattr(data, "texto"):
                        delattr(data, "texto")
                else:
                    data.texto = Base64().decode(texto)
            else:
                data.texto = Base64().decode(texto)

        # Instanciamento de ações
        update_action = GMarcacaoTipoUpdateAction()

        # Retorna o resultado da operação
        return update_action.execute(data)
