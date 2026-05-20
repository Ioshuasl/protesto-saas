from pydantic import BaseModel
from typing import Optional

from actions.data.query_params_parser import QueryParams
from packages.v1.pyros.repository import PyrosRepository


class TPessoaPyrosRepository(PyrosRepository):
    table = "T_PESSOA"
    alias = "TP"
    allowed_fields = {
        "pessoa_id": "TP.PESSOA_ID",
        "pessoa_tipo": "TP.PESSOA_TIPO",
        "nome": "TP.NOME",
        "cpf_cnpj": "TP.CPF_CNPJ",
        "data_nascimento": "TP.DATA_NASCIMENTO",
        "sexo": "TP.SEXO",
        "nacionalidade": "TP.NACIONALIDADE",
        "naturalidade": "TP.NATURALIDADE",
        "email": "TP.EMAIL",
        "telefone": "TP.TELEFONE",
        "endereco": "TP.ENDERECO",
        "numero_end": "TP.NUMERO_END",
        "bairro": "TP.BAIRRO",
        "cidade": "TP.CIDADE",
        "uf": "TP.UF",
        "cep": "TP.CEP",
        "pessoa_cartao_id": "TPC.pessoa_cartao_id",
    }


# ----------------------------------------------------
# Schema base
# ----------------------------------------------------
class TPessoaSchema(BaseModel):
    pessoa_id: Optional[int] = None
    pessoa_tipo: Optional[str] = None
    nome: Optional[str] = None
    nome_fantasia: Optional[str] = None
    nacionalidade: Optional[str] = None

    data_cadastro: Optional[str] = None
    data_auteracao: Optional[str] = None
    data_envioccn: Optional[str] = None
    data_nascimento: Optional[str] = None

    telefone: Optional[str] = None
    ddd: Optional[int] = None

    endereco: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None
    cep: Optional[str] = None

    municipio_id: Optional[int] = None

    cpf_cnpj: Optional[str] = None
    cpf_terceiro: Optional[str] = None

    documento: Optional[str] = None
    documento_numero: Optional[str] = None
    documento_orgao: Optional[str] = None
    documento_uf: Optional[str] = None

    documento_expedicao: Optional[str] = None
    documento_validade: Optional[str] = None

    observacao: Optional[str] = None
    texto: Optional[str] = None

    tb_documentotipo_id: Optional[int] = None
    tb_profissao_id: Optional[int] = None
    tb_estadocivil_id: Optional[int] = None
    tb_regimecomunhao_id: Optional[int] = None

    pessoa_conjuge_id: Optional[int] = None
    pessoa_conjuge_nome: Optional[str] = None

    estrangeiro_nat: Optional[str] = None
    estrangeiro_nat_tb_pais_id: Optional[int] = None
    estrangeiro_res_tb_pais_id: Optional[int] = None
    estrangeiro_res: Optional[str] = None

    enviado_cnncnb: Optional[str] = None
    ccnregistros_id: Optional[int] = None

    observacao_envioccn: Optional[str] = None
    observacao_envio_ccn: Optional[str] = None

    tb_tipologradouro_id: Optional[int] = None
    unidade: Optional[str] = None
    numero_end: Optional[int] = None

    uf_residencia: Optional[str] = None
    naturalidade: Optional[str] = None
    cidade_nat_id: Optional[int] = None

    cert_casamento_numero: Optional[str] = None
    cert_casamento_folha: Optional[str] = None
    cert_casamento_livro: Optional[str] = None
    cert_casamento_cartorio: Optional[str] = None
    cert_casamento_data: Optional[str] = None
    cert_casamento_lei: Optional[str] = None

    nome_pai: Optional[str] = None
    nome_mae: Optional[str] = None

    sexo: Optional[str] = None
    grau_instrucao: Optional[int] = None

    deficiencias: Optional[str] = None

    email: Optional[str] = None

    foto: Optional[str] = None
    biometria: Optional[str] = None

    inscricao_municipal: Optional[str] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um tipo especifico pelo ID (GET)
# ----------------------------------------------------
class TPessoaIdSchema(BaseModel):
    pessoa_id: int

    class Config:
        from_attributes = True


class TPessoaSaveFotoSchema(BaseModel):
    pessoa_id: int
    foto: str

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um tipo especifico pelo ID (GET)
# ----------------------------------------------------
class TPessoaNameSchema(BaseModel):
    nome: str

    class Config:
        from_attributes = True


class TPessoaEmailSchema(BaseModel):
    email: str

    class Config:
        from_attributes = True


class TPessoaCpfSchema(BaseModel):
    cpf: str

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um tipo especifico pelo ID (GET)
# ----------------------------------------------------
class TPessoaTipoSchema(BaseModel):
    pessoa_tipo: str
    query_params: Optional[QueryParams] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para criação de pessoa (POST)
# ----------------------------------------------------
class TPessoaSaveSchema(TPessoaSchema):

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para atualização de pessoa (PUT)
# ----------------------------------------------------
class TPessoaUpdateSchema(TPessoaSchema):

    class Config:
        from_attributes = True
