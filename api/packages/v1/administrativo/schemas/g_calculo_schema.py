from decimal import Decimal
from pydantic import BaseModel, ConfigDict
from typing import Optional


class GCalculoRapidoSchema(BaseModel):

    apresentante: Optional[str] = None
    observacao: Optional[str] = None
    quantidade: Optional[int] = None
    emolumento_id: Optional[float] = None
    valor_documento: Optional[float] = None

    class Config:
        from_attributes = True


class GCalculoServico(BaseModel):

    sistema_id: Optional[float] = None
    emolumento_id: Optional[float] = None
    codigo_tabela: Optional[float] = None
    valor_documento: Optional[Decimal] = None
    quantidade: Optional[Decimal] = None

    # valida e coerce em atribuições após criar o objeto
    model_config = ConfigDict(from_attributes=True, validate_assignment=True)


class ResponseGCalculoRapidoSchema(GCalculoRapidoSchema):

    valor_emolumento: Optional[float] = None
    valor_taxa_judiciaria: Optional[float] = None
    valor_fundos: Optional[float] = None
    valor_iss: Optional[float] = None
    valor_total: Optional[float] = None

    # valida e coerce em atribuições após criar o objeto
    model_config = ConfigDict(from_attributes=True, validate_assignment=True)
