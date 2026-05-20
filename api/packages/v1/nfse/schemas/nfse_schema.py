from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class NfseSchema(BaseModel):
    id_nfse: Optional[int] = None
    data_hora: Optional[datetime] = None
    numnfse: Optional[int] = None
    dataemissao: Optional[datetime] = None
    total_servicos: Optional[Decimal] = None
    total_deducoes: Optional[Decimal] = None
    total_liquido: Optional[Decimal] = None
    valor_iss: Optional[Decimal] = None
    tomador_razao_social: Optional[str] = None
    tomador_cnpj: Optional[str] = None
    tomador_email: Optional[str] = None
    tomador_telefone: Optional[str] = None
    id_cliente: Optional[int] = None
    id_parametros: Optional[int] = None

    class Config:
        from_attributes = True


class NfseIdSchema(BaseModel):
    id_nfse: int


class NfseSaveSchema(BaseModel):
    id_nfse: Optional[int] = None
    data_hora: Optional[datetime] = None
    id_parametros: Optional[int] = None
    id_cliente: Optional[int] = None
    numnfse: Optional[int] = None
    serie: Optional[str] = None
    dataemissao: Optional[datetime] = None
    total_servicos: Optional[Decimal] = None
    total_deducoes: Optional[Decimal] = None
    total_cofins: Optional[Decimal] = None
    total_inss: Optional[Decimal] = None
    total_ir: Optional[Decimal] = None
    total_csll: Optional[Decimal] = None
    total_iss_retido: Optional[Decimal] = None
    outras_retencoes: Optional[Decimal] = None
    desconto_incondicionado: Optional[Decimal] = None
    desconto_condidionado: Optional[Decimal] = None
    base_calculo: Optional[Decimal] = None
    aliquota: Optional[Decimal] = None
    total_liquido: Optional[Decimal] = None
    cod_cnae: Optional[str] = None
    cod_trib_mun: Optional[str] = None
    valor_iss: Optional[Decimal] = None
    discriminacao: Optional[str] = None
    codigo_municipio: Optional[int] = None
    codigo_pais: Optional[int] = None
    cod_mun_incid: Optional[int] = None
    prestador_cnpj: Optional[str] = None
    prestador_im: Optional[str] = None
    prestador_cod_uf: Optional[int] = None
    prestador_codmun: Optional[int] = None
    prestador_razao_social: Optional[str] = None
    tomador_razao_social: Optional[str] = None
    tomador_cnpj: Optional[str] = None
    tomador_im: Optional[str] = None
    tomador_complemento: Optional[str] = None
    tomador_email: Optional[str] = None
    tomador_telefone: Optional[str] = None
    tomador_endereco: Optional[str] = None
    tomador_numend: Optional[str] = None
    tomador_bairro: Optional[str] = None
    tomador_uf: Optional[str] = None
    tomador_codpais: Optional[int] = None
    tomador_cep: Optional[str] = None
    tomador_pais: Optional[str] = None
    tomador_ie: Optional[str] = None
    tomador_codmun: Optional[int] = None
    dt_aprovado: Optional[datetime] = None
    numero_rps: Optional[int] = None
    numero_verificacao: Optional[str] = None
    item_lista: Optional[str] = None
    total_pis: Optional[Decimal] = None
    natureza_operacao: Optional[int] = None
    regime_trib: Optional[int] = None
    iss_retido: Optional[int] = None
    nome_prefeitura: Optional[str] = None
    codigo_cancelamento: Optional[str] = None
    link: Optional[str] = None
    prestador_mail: Optional[str] = None
    prestador_telefone: Optional[str] = None
    prestador_cep: Optional[str] = None
    incidencia_iss: Optional[str] = None
    codigo_nbs: Optional[str] = None
    ent_gov: Optional[str] = None
    class_trib: Optional[str] = None
    tomador_municipio: Optional[str] = None
    data_cancelamento: Optional[datetime] = None
    simples_nacional: Optional[str] = None
    prestador_fantasia: Optional[str] = None
    prestador_endereco: Optional[str] = None
    prestador_num_endereco: Optional[str] = None
    prestador_complemento_end: Optional[str] = None
    prestador_uf: Optional[str] = None
    prestador_bairro: Optional[str] = None
    descricao_item_lista: Optional[str] = None
    indicador_operacao: Optional[str] = None


class NfseUpdateSchema(BaseModel):
    total_servicos: Optional[Decimal] = None
    total_deducoes: Optional[Decimal] = None
    total_liquido: Optional[Decimal] = None
    valor_iss: Optional[Decimal] = None
    discriminacao: Optional[str] = None
