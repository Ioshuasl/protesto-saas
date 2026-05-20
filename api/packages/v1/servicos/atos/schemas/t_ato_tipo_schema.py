from pydantic import BaseModel
from typing import Optional
from decimal import Decimal


# ----------------------------------------------------
# Schema base - representa a tabela T_ATO_TIPO
# ----------------------------------------------------
class TAtoTipoSchema(BaseModel):
    ato_tipo_id: Optional[Decimal] = None
    descricao: Optional[str] = None
    emolumento_id: Optional[Decimal] = None
    livro_natureza_id: Optional[Decimal] = None
    possui_imovel: Optional[str] = None
    situacao: Optional[str] = None
    informar_doi: Optional[str] = None
    natureza_titulo_id: Optional[Decimal] = None
    codigo_doi: Optional[Decimal] = None
    tipo_cobranca: Optional[str] = None
    somente_outorgante: Optional[str] = None
    vinculo_parteimovel_auto: Optional[str] = None
    somente_sistema: Optional[str] = None
    complemento_servico_id: Optional[Decimal] = None
    complemento_tipo_cobranca: Optional[str] = None
    travar_texto: Optional[str] = None
    ordem_qualificacao: Optional[str] = None
    ato_substabelecido_possui: Optional[str] = None
    permite_substabelecer: Optional[str] = None
    emolumento_auxiliar_id: Optional[Decimal] = None
    censec_id: Optional[Decimal] = None
    censec_tipoato_id: Optional[Decimal] = None
    censec_tiponatureza_id: Optional[Decimal] = None
    emolumento_id_2: Optional[Decimal] = None
    tipo_finalizacao_livro: Optional[Decimal] = None
    tipo_finalizacao_traslado: Optional[Decimal] = None
    vincula_falecido: Optional[str] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um registro pelo ID (GET /{id})
# ----------------------------------------------------
class TAtoTipoIdSchema(BaseModel):
    ato_tipo_id: Decimal

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para criação (POST)
# ----------------------------------------------------
class TAtoTipoSaveSchema(TAtoTipoSchema):
    pass


# ----------------------------------------------------
# Schema para atualização (PUT)
# ----------------------------------------------------
class TAtoTipoUpdateSchema(TAtoTipoSchema):
    pass
