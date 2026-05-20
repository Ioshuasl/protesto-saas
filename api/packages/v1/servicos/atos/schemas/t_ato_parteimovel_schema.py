from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


# ----------------------------------------------------
# Schema base - representa a tabela T_ATO_PARTEIMOVEL
# ----------------------------------------------------
class TAtoParteImovelSchema(BaseModel):
    ato_parteimovel_id: Optional[Decimal] = None
    """Auditoria / histórico — sem coluna em T_ATO_PARTEIMOVEL."""
    usuario_id: Optional[Decimal] = None
    ato_vinculoparte_id: Optional[Decimal] = None
    ato_vinculoimovel_id: Optional[Decimal] = None
    ato_id: Optional[Decimal] = None
    participacao: Optional[Decimal] = None
    tipo_proprietario: Optional[str] = None
    qualificacao_onr: Optional[Decimal] = None

    # Campos retornados pelo SQL de indexação (JOINs)
    pessoa_nome: Optional[str] = None
    requerente: Optional[str] = None
    assinatura_tipo: Optional[str] = None
    pessoa_cpf: Optional[str] = None
    ato_partetipo_descricao: Optional[str] = None
    imovel_matricula: Optional[str] = None
    numero_unidade: Optional[str] = None
    quadra: Optional[str] = None
    area: Optional[Decimal] = None
    logradouro: Optional[str] = None

    class Config:
        from_attributes = True


class TAtoParteImovelIndexSchema(BaseModel):
    ato_id: Decimal

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um registro pelo ID (GET /{id})
# ----------------------------------------------------
class TAtoParteImovelIdSchema(BaseModel):
    ato_parteimovel_id: Decimal
    usuario_id: Optional[Decimal] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para criação (POST)
# ----------------------------------------------------
class TAtoParteImovelSaveSchema(TAtoParteImovelSchema):
    pass


# ----------------------------------------------------
# Schema para atualização (PUT)
# ----------------------------------------------------
class TAtoParteImovelUpdateSchema(TAtoParteImovelSchema):
    pass
