from actions.data.qrcode import QRCode
from actions.data.text import Text
from packages.v1.resolver.actions.resolver_dynamic_sql_action import (
    ResolverDynamicSqlAction,
)
from schemas.qrcode_schema import QrCodeSchema


class ResolverTextoFillerService:
    @staticmethod
    def _read(source, key: str, default=None):
        if isinstance(source, dict):
            return source.get(key, default)
        return getattr(source, key, default)

    def execute(self, data):

        # Classe que busca em qualquer tabela
        dynamic_sql_action = ResolverDynamicSqlAction()

        # Montaa e executa os valores
        response = dynamic_sql_action.execute(data.texto)

        # Extrai o texto puro
        response = Text.plain(response)

        # Obtem as marcações com valores corretos
        prefixo = getattr(data.texto, "prefixo", "")
        sufixo = getattr(data.texto, "sufixo", "")

        # Monta o valor completo
        response = f"{prefixo}{response}{sufixo}"

        # Verifica o tipo de saída da informação
        if getattr(data.texto, "output", None):

            # Verifica se a saída é do tipo qrcode
            if getattr(data.texto.output, "qrcode", None):
                qrcode_output = data.texto.output.qrcode
                qrcode_config = self._read(qrcode_output, "config", None)
                qrcode_image = self._read(qrcode_output, "image", None)

                response_binary = QRCode.execute(
                    QrCodeSchema(
                        data=response,
                        box_size=self._read(qrcode_config, "box_size", 10),
                        border=self._read(qrcode_config, "border", 4),
                        output="binary",
                        image_format=self._read(qrcode_image, "format", "PNG"),
                        fill_color=self._read(qrcode_image, "fill_color", "black"),
                        back_color=self._read(qrcode_image, "back_color", "white"),
                    )
                )

                response = {
                    "__type__": "image",
                    "bytes": response_binary,
                    "format": self._read(qrcode_image, "format", "PNG"),
                }

        # Retorna os valores
        return response
