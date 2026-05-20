import base64
from io import BytesIO

from docx import Document
from fastapi import HTTPException, status

from actions.data.base64 import Base64
from actions.data.text import Text
from packages.v1.ged.actions.ged_docx_page_setup_action import (
    GEDDocxPageSetupAction,
)
from packages.v1.ged.schemas.ged_schema import GEDDocxPageSetupSchema
from packages.v1.administrativo.schemas.t_minuta_schema import TMinutaIdSchema
from packages.v1.administrativo.services.t_minuta.go.t_minuta_show_service import (
    ShowService,
)
from packages.v1.servicos.atos.actions.t_ato.t_ato_update_minuta_action import (
    TAtoUpdateMinutaAction,
)
from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoSaveMinuta


class TAtoUpdateMinutaService:
    """
    Serviço responsável pela operação de atualização de um registro
    na tabela T_ATO.
    """

    def execute(self, data: TAtoSaveMinuta):

        response_minuta = ShowService().execute(
            TMinutaIdSchema(
                minuta_id=data.minuta_id,
            )
        )

        if not response_minuta:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Nao foi possivel processar o texto da minuta. Revise os dados e tente novamente.",
            )

        data.texto = base64.b64decode(response_minuta.texto)

        # Atualiza a minuta do ato
        response = TAtoUpdateMinutaAction().execute(data)

        if not response.texto:

            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Nao foi possivel atualizar o texto da minuta no momento.",
            )

        if response.texto:

            response.texto = None

        # ----------------------------------------------------
        # Execução da ação e retorno do resultado
        # ----------------------------------------------------
        return response
