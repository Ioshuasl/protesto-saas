from pydantic import BaseModel
from typing import Optional

# Função de sanitização

# ----------------------------------------------------
# Schema base para TImovelUnidade
# ----------------------------------------------------
class TImovelUnidadeSchema(BaseModel):
    imovel_unidade_id: Optional[int] = None
    imovel_id: Optional[int] = None
    numero_unidade: Optional[str] = None
    quadra: Optional[str] = None
    area: Optional[float] = None
    superquadra: Optional[str] = None
    conjunto: Optional[str] = None
    bloco: Optional[str] = None
    area_descritiva: Optional[str] = None
    caracteristica: Optional[str] = None
    reserva_florestal: Optional[str] = None
    geo_referenciamento: Optional[str] = None
    logradouro: Optional[str] = None
    tb_tipologradouro_id: Optional[int] = None
    selecionado: Optional[str] = None
    complemento: Optional[str] = None
    tipo_imovel: Optional[int] = None
    tipo_construcao: Optional[int] = None
    texto: Optional[bytes] = None
    numero_edificacao: Optional[str] = None
    iptu: Optional[str] = None
    ccir: Optional[str] = None
    nirf: Optional[str] = None
    lote: Optional[str] = None
    torre: Optional[str] = None
    nomeloteamento: Optional[str] = None
    nomecondominio: Optional[str] = None
    numero: Optional[float] = None
    cnm_numero: Optional[str] = None
    imovel_publico_uniao: Optional[str] = None
    spu_rip: Optional[str] = None
    cat: Optional[str] = None
    inscricao_municipal: Optional[str] = None
    cib: Optional[str] = None
    area_construida: Optional[float] = None

    class Config:
        from_attributes = True

# ----------------------------------------------------
# Schema base para TImovelUnidadeIndex
# ----------------------------------------------------
class TImovelUnidadeIndexSchema(BaseModel):
    imovel_id: Optional[int] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar uma unidade pelo ID (GET)
# ----------------------------------------------------
class TImovelUnidadeIdSchema(BaseModel):
    imovel_unidade_id: int


# ----------------------------------------------------
# Schema para criação de nova unidade (POST)
# ----------------------------------------------------
class TImovelUnidadeSaveSchema(BaseModel):
    imovel_id: Optional[int] = None
    imovel_unidade_id: Optional[int] = None
    numero_unidade: Optional[str] = None
    area: Optional[float] = None
    logradouro: Optional[str] = None
    tb_tipologradouro_id: Optional[int] = None
    texto: Optional[bytes] = None

    # Outros campos opcionais
    quadra: Optional[str] = None
    superquadra: Optional[str] = None
    conjunto: Optional[str] = None
    bloco: Optional[str] = None
    area_descritiva: Optional[str] = None
    caracteristica: Optional[str] = None
    reserva_florestal: Optional[str] = None
    geo_referenciamento: Optional[str] = None
    selecionado: Optional[str] = None
    complemento: Optional[str] = None
    tipo_imovel: Optional[int] = None
    tipo_construcao: Optional[int] = None
    numero_edificacao: Optional[str] = None
    iptu: Optional[str] = None
    ccir: Optional[str] = None
    nirf: Optional[str] = None
    lote: Optional[str] = None
    torre: Optional[str] = None
    nomeloteamento: Optional[str] = None
    nomecondominio: Optional[str] = None
    numero: Optional[float] = None
    cnm_numero: Optional[str] = None
    imovel_publico_uniao: Optional[str] = None
    spu_rip: Optional[str] = None
    cat: Optional[str] = None
    inscricao_municipal: Optional[str] = None
    cib: Optional[str] = None
    area_construida: Optional[float] = None

    class Config:
        from_attributes = True

# ----------------------------------------------------
# Schema para atualização de unidade (PUT)
# ----------------------------------------------------
class TImovelUnidadeUpdateSchema(BaseModel):
    imovel_unidade_id: Optional[int] = None
    imovel_id: Optional[int] = None
    numero_unidade: Optional[str] = None
    area: Optional[float] = None
    logradouro: Optional[str] = None
    tb_tipologradouro_id: Optional[int] = None
    texto: Optional[bytes] = None
    quadra: Optional[str] = None
    superquadra: Optional[str] = None
    conjunto: Optional[str] = None
    bloco: Optional[str] = None
    area_descritiva: Optional[str] = None
    caracteristica: Optional[str] = None
    reserva_florestal: Optional[str] = None
    geo_referenciamento: Optional[str] = None
    selecionado: Optional[str] = None
    complemento: Optional[str] = None
    tipo_imovel: Optional[int] = None
    tipo_construcao: Optional[int] = None
    numero_edificacao: Optional[str] = None
    iptu: Optional[str] = None
    ccir: Optional[str] = None
    nirf: Optional[str] = None
    lote: Optional[str] = None
    torre: Optional[str] = None
    nomeloteamento: Optional[str] = None
    nomecondominio: Optional[str] = None
    numero: Optional[float] = None
    cnm_numero: Optional[str] = None
    imovel_publico_uniao: Optional[str] = None
    spu_rip: Optional[str] = None
    cat: Optional[str] = None
    inscricao_municipal: Optional[str] = None
    cib: Optional[str] = None
    area_construida: Optional[float] = None

    class Config:
        from_attributes = True