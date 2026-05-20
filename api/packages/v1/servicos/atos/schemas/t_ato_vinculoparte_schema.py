from firebird.driver.fbapi import Int
from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime


# ----------------------------------------------------
# Schema base - representa a tabela T_ATO_VINCULOPARTE
# ----------------------------------------------------
class TAtoVinculoParteSchema(BaseModel):
    ato_vinculoparte_id: Optional[Decimal] = None
    usuario_id: Optional[Decimal] = None
    pessoa_id: Optional[Decimal] = None
    ato_id: Optional[Decimal] = None
    ato_partetipo_id: Optional[Decimal] = None
    tb_estadocivil_id: Optional[Decimal] = None
    tb_profissao_id: Optional[Decimal] = None
    marcacao_tipo_id: Optional[Decimal] = None

    pessoa_nome: Optional[str] = None
    tipo_vinculo: Optional[str] = None
    participacao: Optional[Decimal] = None
    assinatura_tipo: Optional[str] = None

    pessoa_conjuge_id: Optional[Decimal] = None
    vinculo_conjuge: Optional[str] = None
    auxiliar_id: Optional[Decimal] = None
    ordem: Optional[Decimal] = None

    pessoa_cpf: Optional[str] = None
    tipo_vinculo_auxiliar: Optional[str] = None

    texto_complementar: Optional[bytes] = None

    tb_regimecomunhao_id: Optional[Decimal] = None
    requerente: Optional[str] = None

    descrever: Optional[str] = None
    autorizacao: Optional[str] = None
    declaracao: Optional[str] = None

    vbotao: Optional[str] = None
    numero: Optional[str] = None
    tiporegistro: Optional[Decimal] = None

    orgao: Optional[str] = None
    formaregistro: Optional[str] = None
    numerolivro: Optional[str] = None

    folha: Optional[Decimal] = None
    numeroregistro: Optional[Decimal] = None
    dataregistro: Optional[datetime] = None

    qualificacao_onr: Optional[Decimal] = None

    texto_qualificacao: Optional[bytes] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um registro pelo ID (GET /{id})
# ----------------------------------------------------
class TAtoVinculoParteIndexSchema(BaseModel):
    ato_id: Decimal

    class Config:
        from_attributes = True

# ----------------------------------------------------
# Schema para localizar um registro pelo ID (GET /{id})
# ----------------------------------------------------
class TAtoVinculoParteIndexByTipoVinculoSchema(BaseModel):
    ato_id: Decimal
    tipo_vinculo: int

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um registro pelo ID (GET /{id})
# ----------------------------------------------------
class TAtoVinculoParteIdSchema(BaseModel):
    ato_vinculoparte_id: Decimal
    usuario_id: Optional[Decimal] = None

    class Config:
        from_attributes = True


class TAtoVinculoParteTextoQualificacaoSchema(BaseModel):
    ato_vinculoparte_id: Decimal
    marcacao_tipo_id: Optional[Decimal] = None
    texto_qualificacao: Optional[bytes] = None

    class Config:
        from_attributes = True


class TAtoVinculoParteTextoQualificacaoUpdateSchema(BaseModel):
    ato_vinculoparte_id: Optional[Decimal] = None
    texto_qualificacao: Optional[bytes] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para criação (POST)
# ----------------------------------------------------
class TAtoVinculoParteSaveSchema(TAtoVinculoParteSchema):
    pass


# ----------------------------------------------------
# Schema para atualização (PUT)
# ----------------------------------------------------
class TAtoVinculoParteUpdateSchema(TAtoVinculoParteSchema):
    pass
