from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ----------------------------------------------------
# Schema para localizar um registro pelo ID (GET /{id})
# ----------------------------------------------------
class TPessoaCartaoIndexchema(BaseModel):
    pessoa_id: int

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema base - representa a tabela PESSOA_CARTAO
# ----------------------------------------------------
class TPessoaCartaoSchema(BaseModel):
    pessoa_cartao_id: Optional[int] = None
    data_abertura: Optional[datetime] = None
    usuario_id: Optional[int] = None
    situacao: Optional[str] = None
    cartao_impresso: Optional[str] = None
    pessoa_id: Optional[int] = None
    renovado: Optional[str] = None
    numero: Optional[int] = None
    tipo_pessoa_relacionada: Optional[str] = None
    id_cartao: Optional[int] = None
    data_renovacao: Optional[datetime] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um registro pelo ID (GET /{id})
# ----------------------------------------------------
class TPessoaCartaoIdSchema(BaseModel):
    pessoa_cartao_id: int

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para criação (POST)
#  - normalmente sem o ID (gerado pelo banco)
# ----------------------------------------------------
class TPessoaCartaoSaveSchema(TPessoaCartaoSchema):

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para atualização (PUT)
#  - inclui o ID + campos opcionais para alterar
# ----------------------------------------------------
class TPessoaCartaoUpdateSchema(TPessoaCartaoSchema):

    class Config:
        from_attributes = True
