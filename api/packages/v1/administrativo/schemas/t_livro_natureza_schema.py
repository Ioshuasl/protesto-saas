from decimal import Decimal
import string
from typing import Optional

from pydantic import BaseModel


class TLivroNaturezaSchema(BaseModel):
    livro_natureza_id: Optional[Decimal] = None
    natureza_id: Optional[Decimal] = None
    descricao: Optional[str] = None
    frente_verso: Optional[str] = None
    parte_assina: Optional[str] = None
    tipo_finalizacao_livro: Optional[Decimal] = None
    assinatura_impressa: Optional[str] = None
    controle_usuario: Optional[str] = None
    tipo_finalizacao_traslado: Optional[Decimal] = None
    livro_alternado: Optional[Decimal] = None
    livro_lavratura: Optional[Decimal] = None
    tipo_cabecalho: Optional[str] = None
    tipo_rodape: Optional[str] = None
    tipo_cabecalho_auxiliar: Optional[str] = None
    folha_anterior: Optional[Decimal] = None
    livro_anterior: Optional[Decimal] = None
    texto_oficial_certidao: Optional[Decimal] = None
    sigla_natureza: Optional[str] = None
    tipo_cabecalho_sec: Optional[str] = None
    tipo_cabecalho_auxiliar_sec: Optional[str] = None
    tipo_rodape_sec: Optional[str] = None
    usar_cabecalho_secundario: Optional[str] = None
    cabecalho_primeira_pagina: Optional[str] = None
    cabecalho_primeira_pagina_aux: Optional[str] = None
    livro_inicial_frenteverso: Optional[Decimal] = None
    tipo_cabecalho_auxanterior: Optional[str] = None
    somente_livro: Optional[str] = None
    assinatura_oficial: Optional[str] = None
    ajuste_verso_livro: Optional[Decimal] = None
    ajuste_verso_traslado: Optional[Decimal] = None
    c_ato_frenteverso_anterior: Optional[str] = None
    chave_importacao: Optional[Decimal] = None
    tipo_cabecalho_pdf: Optional[str] = None
    tipo_cabeca_aux_pdf: Optional[str] = None
    cabec_primeira_pag_pdf: Optional[str] = None
    tipo_rodape_pdf: Optional[str] = None
    tipo_cabec_sec_pdf: Optional[str] = None
    tipo_cabec_auxiliar_sec_pdf: Optional[str] = None
    cabec_primeira_pagina_aux_pdf: Optional[str] = None
    tipo_rodape_sec_pdf: Optional[str] = None
    permite_restricao: Optional[str] = None
    modelo_livro: Optional[bytes] = None
    modelo_traslado: Optional[bytes] = None

    class Config:
        from_attributes = True


class TLivroNaturezaIdSchema(BaseModel):
    livro_natureza_id: Decimal

    class Config:
        from_attributes = True

class TLivroNaturezaShowModeloSchema(BaseModel):
    livro_natureza_id: Optional[Decimal] = None
    modelo: Optional[Decimal] = None
    coluna: Optional[str] = None

    class Config:
        from_attributes = True

class TLivroNaturezaUpdateModeloSchema(BaseModel):
    livro_natureza_id: Optional[Decimal] = None
    modelo_texto: Optional[bytes] = None
    coluna: Optional[str] = None

    class Config:
        from_attributes = True

class TLivroNaturezaSaveSchema(TLivroNaturezaSchema):
    pass

class TLivroNaturezaUpdateSchema(TLivroNaturezaSchema):
    pass

