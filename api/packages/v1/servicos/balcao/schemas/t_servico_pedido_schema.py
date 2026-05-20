from pydantic import BaseModel
from typing import Annotated, List, Optional
from decimal import Decimal
from datetime import datetime

from pydantic.config import ConfigDict
from pydantic.functional_validators import BeforeValidator

from packages.v1.parametros.schemas.g_config_schema import GConfigNomeSchema
from packages.v1.servicos.balcao.schemas.t_servico_itempedido_schema import (
    TServicoItemPedidoSaveSchema,
)


# ---------- Utilidades ----------
def _zero_to_none(v):
    # Trate 0, 0.0, "0", "" como None
    return None if v in (0, 0.0, "0", "", None) else v


def _to_decimal(v):
    if v in (None, "", "0", 0, 0.0):
        return Decimal("0")  # ou None, se preferir
    # Sempre usar str para evitar floating point issues
    return Decimal(str(v))


ZeroNoneInt = Annotated[Optional[int], BeforeValidator(_zero_to_none)]
Money = Annotated[Optional[Decimal], BeforeValidator(_to_decimal)]
Fk = ZeroNoneInt  # só para semântica


class TServicoPedidoSchema(BaseModel):
    servico_pedido_id: Optional[Decimal] = None
    valor_pedido: Optional[Decimal] = None
    valor_pago: Optional[Decimal] = None
    usuario_id: Optional[Decimal] = None
    data_pedido: Optional[datetime] = None
    mensalista_livrocaixa_id: Optional[Decimal] = None
    observacao: Optional[str] = None
    escrevente_id: Optional[Decimal] = None
    situacao: Optional[str] = None
    estornado: Optional[str] = None
    apresentante: Optional[str] = None
    nfse_id: Optional[Decimal] = None
    pessoa_id_nfse: Optional[Decimal] = None
    cpfcnpj_apresentante: Optional[str] = None
    itens: Optional[List[TServicoItemPedidoSaveSchema]] = None

    model_config = ConfigDict(from_attributes=True)


class TServicoPedidoIdSchema(BaseModel):
    servico_pedido_id: Decimal
    model_config = ConfigDict(from_attributes=True)


class TServicoPedidoSaveSchema(TServicoPedidoSchema):

    model_config = ConfigDict(from_attributes=True)


class TServicoPedidoSituacaoSchema(BaseModel):

    servico_pedido_id: int = None
    usuario_id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)


class TServicoPedidoSaveSituacaoSchema(BaseModel):

    servico_pedido_id: int = None
    situacao: str = None

    model_config = ConfigDict(from_attributes=True)


class TServicoPedidoUpdateSchema(TServicoPedidoSchema):

    model_config = ConfigDict(from_attributes=True)


class TServicoPedidoUpdateValorTotal(BaseModel):

    servico_pedido_id: Optional[Decimal] = None
    valor_pedido: Optional[Decimal] = None
    valor_pago: Optional[Decimal] = None
    operacao: int = None

    model_config = ConfigDict(from_attributes=True)


class TServicoPedidoLoadParams(GConfigNomeSchema):
    model_config = ConfigDict(from_attributes=True)
