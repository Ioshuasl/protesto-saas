import base64
import json
import re
from types import SimpleNamespace
from packages.v1.administrativo.controllers.g_marcacao_tipo_controller import (
    GMarcacaoTipoGetByNomeService,
)
from packages.v1.administrativo.schemas.g_marcacao_tipo_schema import (
    GMarcacaoTipoNomeSchema,
)


class ResolverBuscarMarcacaoService:

    @staticmethod
    def _to_namespace(value):
        if isinstance(value, dict):
            return SimpleNamespace(
                **{
                    key: ResolverBuscarMarcacaoService._to_namespace(val)
                    for key, val in value.items()
                }
            )
        if isinstance(value, list):
            return [ResolverBuscarMarcacaoService._to_namespace(item) for item in value]
        return value

    @staticmethod
    def parse_texto_blob(value: bytes) -> dict:
        text = value.decode("utf-8", errors="ignore")
        text = re.sub(r"[\x00-\x1F\x7F-\x9F]", "", text)
        data = json.loads(text)
        return ResolverBuscarMarcacaoService._to_namespace(data)

    def execute(self, data: GMarcacaoTipoNomeSchema):

        # Classe para buscar por nome de macação
        marcacao_tipo_get_by_nome_service = GMarcacaoTipoGetByNomeService()

        # Retorna o resultado da operação
        response = marcacao_tipo_get_by_nome_service.execute(data, False)

        if getattr(response, "texto", None):

            # Normaliza o texto
            response.texto = self.parse_texto_blob(base64.b64decode(response.texto))

        return response
