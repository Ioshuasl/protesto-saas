from pydantic import BaseModel
from typing import Optional


# ----------------------------------------------------
# Schema base - representa a tabela G_EMOLUMENTO_ITEM
# ----------------------------------------------------
class GEmolumentoItemSchema(BaseModel):
    valor_emolumento: Optional[float] = None
    emolumento_item_id: Optional[float] = None
    emolumento_id: Optional[float] = None
    valor_inicio: Optional[float] = None
    valor_fim: Optional[float] = None
    valor_taxa_judiciaria: Optional[float] = None
    emolumento_periodo_id: Optional[float] = None
    codigo: Optional[float] = None
    pagina_extra: Optional[float] = None
    valor_pagina_extra: Optional[float] = None
    valor_outra_taxa1: Optional[float] = None
    codigo_selo: Optional[str] = None
    valor_fundo_ri: Optional[float] = None
    codigo_tabela: Optional[str] = None
    selo_grupo_id: Optional[float] = None
    codigo_km: Optional[str] = None
    emolumento_acresce: Optional[float] = None
    taxa_acresce: Optional[float] = None
    funcivil_acresce: Optional[float] = None
    valor_fracao: Optional[float] = None
    valor_por_excedente_emol: Optional[float] = None
    valor_por_excedente_tj: Optional[float] = None
    valor_por_excedente_fundo: Optional[float] = None
    valor_limite_excedente_emol: Optional[float] = None
    valor_limite_excedente_tj: Optional[float] = None
    valor_limite_excedente_fundo: Optional[float] = None
    fundo_selo: Optional[float] = None
    distribuicao: Optional[float] = None
    vrcext: Optional[float] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um registro pelo ID (GET /{id})
# ----------------------------------------------------
class GEmolumentoItemIdSchema(BaseModel):
    emolumento_item_id: float

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um registro pelo EmolumentoId (GET /{id})
# ----------------------------------------------------
class GEmolumentoItemIndexSchema(BaseModel):
    emolumento_id: float
    emolumento_periodo_id: float

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um registro pelo EmolumentoId (GET /{id})
# ----------------------------------------------------
class GEmolumentoItemByTipoAtoSchema(BaseModel):
    emolumento_periodo_id: float = None
    numero: int = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para criação (POST)
# ----------------------------------------------------
class GEmolumentoItemSaveSchema(GEmolumentoItemSchema):
    pass


# ----------------------------------------------------
# Schema para atualização (PUT)
# ----------------------------------------------------
class GEmolumentoItemUpdateSchema(GEmolumentoItemSchema):
    pass
