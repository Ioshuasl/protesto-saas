from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class ParametrosSchema(BaseModel):
    id_parametros: Optional[int] = None
    razao_social: Optional[str] = None
    codigo_ibge: Optional[int] = None
    cnpj: Optional[str] = None
    cep: Optional[str] = None
    im: Optional[str] = None
    codigo_uf: Optional[int] = None
    cnae: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    simples_nacional: Optional[str] = None
    serie: Optional[str] = None
    aliquota_iss: Optional[Decimal] = None
    class_tributaria: Optional[str] = None
    codigo_nbs: Optional[str] = None
    item_lista: Optional[str] = None
    natureza_padrao: Optional[int] = None
    nome_prefeitura: Optional[str] = None
    numero_serie_certificado: Optional[str] = None
    uf: Optional[str] = None
    logo_cartorio: Optional[str] = None
    smtp_email: Optional[str] = None
    smtp_corpo_email: Optional[str] = None
    smtp_senha: Optional[str] = None
    smtp_porta: Optional[int] = None
    smtp_ssl: Optional[str] = None
    smtp_tls: Optional[str] = None
    smtp_usuario: Optional[str] = None
    usuario_web_service: Optional[str] = None
    senha_usuario_web_service: Optional[str] = None
    endereco: Optional[str] = None
    numero_endereco: Optional[str] = None
    bairro: Optional[str] = None
    complemento_endereco: Optional[str] = None
    codigo_tributacao: Optional[str] = None
    municipio: Optional[str] = None
    descricao_item_lista: Optional[str] = None
    fantasia: Optional[str] = None
    data_hora: Optional[datetime] = None
    regime_tributario: Optional[int] = None
    indicador_operacao: Optional[str] = None
    smtp_host: Optional[str] = None
    smtp_assunto: Optional[str] = None

    class Config:
        from_attributes = True


class ParametrosIdSchema(BaseModel):
    id_parametros: int


class ParametrosSaveSchema(ParametrosSchema):
    id_parametros: int


class ParametrosUpdateSchema(ParametrosSchema):
    pass

