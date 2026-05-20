from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel
from typing import Optional


# ----------------------------------------------------
# Schema base - representa a tabela de Biometria
# ----------------------------------------------------
class TBiometriaPessoaSchema(BaseModel):
    biometria_pessoa_id: Optional[Decimal] = None
    digital_id: Optional[int] = None
    objeto: Optional[bytes] = None
    chave_id: Optional[Decimal] = None
    imagem_biometria: Optional[bytes] = None
    objeto_backup: Optional[bytes] = None
    objeto_strig_normal: Optional[bytes] = None
    leitorbiometrico: Optional[str] = None
    data_coleta: Optional[datetime] = None
    pessoa_id: Optional[Decimal] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um registro pelo ID (GET /{id})
# ----------------------------------------------------
class TBiometriaPessoaResponseSchema(BaseModel):
    biometria_pessoa_id: Optional[Decimal] = None
    digital_id: Optional[int] = None
    objeto: Optional[str] = None
    chave_id: Optional[Decimal] = None
    imagem_biometria: Optional[str] = None
    objeto_backup: Optional[str] = None
    objeto_strig_normal: Optional[str] = None
    leitorbiometrico: Optional[str] = None
    data_coleta: Optional[datetime] = None
    pessoa_id: Optional[Decimal] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um registro pelo ID (GET /{id})
# ----------------------------------------------------
class TBiometriaPessoaIndexSchema(BaseModel):
    chave_id: Decimal

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um registro pelo ID (GET /{id})
# ----------------------------------------------------
class TBiometriaPessoaIdSchema(BaseModel):
    biometria_pessoa_id: Decimal

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para criação (POST)
# ----------------------------------------------------
class TBiometriaPessoaSaveSchema(TBiometriaPessoaSchema):

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para atualização (PUT)
# ----------------------------------------------------
class TBiometriaPessoaUpdateSchema(TBiometriaPessoaSchema):

    class Config:
        from_attributes = True
