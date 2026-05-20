from urllib import response

from actions.data.base64 import Base64

from fastapi import HTTPException, status

# Importação do Schema ajustada
from packages.v1.administrativo.schemas.g_marcacao_tipo_schema import (
    GMarcacaoTipoIdSchema,
)

# Importação da Action ajustada
from packages.v1.administrativo.actions.g_marcacao_tipo.g_marcacao_tipo_show_action import (
    GMarcacaoTipoShowAction,
)

from packages.v1.docx.services.docx_process_service import (
    DOCXProcess,
    DOCXProcessSchema,
)


class GMarcacaoTipoShowService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela G_MARCACAO_TIPO.
    """

    def execute(self, data: GMarcacaoTipoIdSchema):

        # Instanciamento da ação
        show_action = GMarcacaoTipoShowAction()

        # Executa a ação em questão
        data = show_action.execute(data)

        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar o registro de G_MARCACAO_TIPO",
            )

        # ===============================
        # TRATAMENTO PARA GRUPO TIPO "M"
        # ===============================
        if data.grupo_tipo == "M":

            # Caso não exista conteúdo, evita erro no DOCXProcess
            content = data.texto if data.texto else b""

            data.texto = DOCXProcess().execute(
                DOCXProcessSchema(
                    id=str(data.marcacao_tipo_id),
                    content=content,
                    save_disk=True,
                )
            )

        # ==========================================
        # TRATAMENTO PARA DEMAIS GRUPOS (BASE64)
        # ==========================================
        else:

            if not data.texto:
                # Campo nulo no banco
                data.texto = b""

            elif isinstance(data.texto, bytes):
                # Já é binário vindo do Firebird
                pass

            elif isinstance(data.texto, str):
                try:
                    data.texto = Base64.decode(data.texto)
                except Exception:
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail="Erro ao decodificar conteúdo base64 do campo TEXTO",
                    )

            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Formato inesperado para o campo TEXTO: {type(data.texto)}",
                )

        if isinstance(data.texto, (bytes, bytearray)):
            data.texto = Base64.decode(data.texto)

        # Retorno da informação
        return data
