from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ----------------------------------------------------
# Schema base - representa a tabela G_CARTORIO
# ----------------------------------------------------
class GCartorioSchema(BaseModel):
    cartorio_id: Optional[float] = None
    seq: Optional[str] = None
    cns: Optional[str] = None
    cnpj: Optional[str] = None
    denominacao_serventia: Optional[str] = None
    status_serventia: Optional[float] = None
    atribuicao: Optional[str] = None
    dt_instalacao: Optional[datetime] = None
    dat_inclusao: Optional[datetime] = None
    dat_alteracao: Optional[datetime] = None
    uf: Optional[str] = None
    municipio: Optional[str] = None
    cod_ibge: Optional[float] = None
    bairro: Optional[str] = None
    distrito: Optional[str] = None
    sub_distrito: Optional[str] = None
    endereco: Optional[str] = None
    complemento: Optional[str] = None
    cep: Optional[str] = None
    telefone1: Optional[str] = None
    fax: Optional[str] = None
    email: Optional[str] = None
    home_page: Optional[str] = None
    dt_inativacao: Optional[datetime] = None
    nome_titular: Optional[str] = None
    cpf_titular: Optional[str] = None
    dt_ingresso_titular: Optional[str] = None
    dt_nomeacao_titular: Optional[datetime] = None
    tipo_titular: Optional[float] = None
    forma_ingresso_titular: Optional[float] = None
    dt_assuncao_serventia_titular: Optional[datetime] = None
    dt_colacao_grau_titular: Optional[datetime] = None
    bacharelado_titular: Optional[float] = None
    nome_substituto: Optional[str] = None
    cpf_substituto: Optional[str] = None
    email_substituto: Optional[str] = None
    dat_inclusao_substituto: Optional[datetime] = None
    dat_alteracao_substituto: Optional[datetime] = None
    emitente: Optional[str] = None
    cpf_escrevente: Optional[str] = None
    nome_escrevente: Optional[str] = None
    cargo_tituloar: Optional[str] = None
    endereco_numero: Optional[str] = None
    ddd: Optional[str] = None
    insc_estadual: Optional[str] = None
    insc_municipal: Optional[str] = None
    razao_social: Optional[str] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um registro pelo ID (GET /{id})
# ----------------------------------------------------
class GCartorioIdSchema(BaseModel):
    cartorio_id: float

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para criação (POST)
# ----------------------------------------------------
class GCartorioSaveSchema(GCartorioSchema):
    pass


# ----------------------------------------------------
# Schema para atualização (PUT)
# ----------------------------------------------------
class GCartorioUpdateSchema(GCartorioSchema):
    pass
