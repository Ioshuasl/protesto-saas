from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class TLivroAndamentoSchema(BaseModel):
    livro_andamento_id: Optional[Decimal] = None
    livro_natureza_id: Optional[Decimal] = None
    usuario_id: Optional[Decimal] = None
    folha_atual: Optional[Decimal] = None
    numero_livro: Optional[Decimal] = None
    numero_livro_letra: Optional[str] = None
    data_abertura: Optional[str] = None
    data_fechamento: Optional[str] = None
    numero_folhas: Optional[Decimal] = None
    antigo: Optional[str] = None
    c_ato_frenteverso_atual: Optional[str] = None
    chave_importacao: Optional[Decimal] = None

    class Config:
        from_attributes = True


class TLivroAndamentoIdSchema(BaseModel):
    livro_andamento_id: Decimal

    class Config:
        from_attributes = True


class TLivroAndamentoNaturezaIdSchema(BaseModel):
    livro_natureza_id: Decimal

    class Config:
        from_attributes = True


class TLivroAndamentoSaveSchema(TLivroAndamentoSchema):
    pass


class TLivroAndamentoUpdateSchema(TLivroAndamentoSchema):
    pass
