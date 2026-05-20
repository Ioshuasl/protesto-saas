from types import SimpleNamespace

from actions.data.microtime import Microtime
from actions.data.text import Text
from fastapi import HTTPException, status
from packages.v1.servicos.balcao.actions.t_servico_itempedido.t_servico_itempedido_show_action import (
    TServicoItemPedidoShowAction,
)
from packages.v1.servicos.balcao.schemas.t_servico_itempedido_schema import (
    TServicoItemPedidoIdSchema,
)


class TServicoItemPedidoCertidaoEditService:
    def execute(self, data: TServicoItemPedidoIdSchema):
        row = TServicoItemPedidoShowAction().execute(data)
        data = SimpleNamespace(**row)

        texto = Text.decompress(data.certidao_texto)
        name = f"{data.servico_itempedido_id}_{Microtime.as_int()}.rtf"

        with open("./storage/temp/" + str(name), "wb") as f:
            f.write(texto.encode("utf-8"))

        data.certidao_texto = name

        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nao foi possivel localizar o registro de T_SERVICO_ITEMPEDIDO.",
            )

        return data
