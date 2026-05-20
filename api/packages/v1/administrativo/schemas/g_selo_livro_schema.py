from datetime import datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel


class GSeloLivroSchema(BaseModel):
    selo_livro_id: Optional[int] = None
    numero: Optional[int] = None
    selo_situacao_id: Optional[int] = None
    observacao: Optional[str] = None
    selo_lote_id: Optional[int] = None
    sigla: Optional[str] = None
    descricao: Optional[str] = None
    tabela: Optional[str] = None
    campo_id: Optional[int] = None
    usuario_id: Optional[int] = None
    informado: Optional[str] = None
    data_informacao: Optional[datetime] = None
    reservado: Optional[str] = None
    numero_agrupador: Optional[str] = None
    apresentante: Optional[str] = None
    ip_maquina: Optional[str] = None

    valor_total: Optional[Decimal] = None
    valor_emolumento: Optional[Decimal] = None
    valor_taxa_judiciaria: Optional[Decimal] = None
    valor_fundesp: Optional[Decimal] = None

    data_exportacao: Optional[datetime] = None
    codigo_exportacao: Optional[int] = None
    data: Optional[datetime] = None
    usuario_id_exportacao: Optional[int] = None
    selo_consolidacao_id: Optional[int] = None
    status_consolidacao: Optional[int] = None
    data_recebimento_tj: Optional[datetime] = None

    tag_selo: Optional[bytes] = None
    valor_iss: Optional[Decimal] = None
    validacao: Optional[str] = None
    id_do_ato_isentado: Optional[int] = None
    motivo_isencao: Optional[str] = None
    data_cadastro: Optional[datetime] = None

    iss_cobrado_usuario: Optional[str] = None
    conciliado: Optional[str] = None
    tipo_ato: Optional[int] = None
    nlote: Optional[int] = None
    apontamento_protesto: Optional[int] = None
    valor_ato: Optional[Decimal] = None

    numero_livro: Optional[str] = None
    numero_folhas: Optional[str] = None
    valor_informacoes_centrais: Optional[Decimal] = None
    envio_imediato: Optional[str] = None
    protocolo: Optional[int] = None
    cpfcnpj: Optional[str] = None
    cartorio_origem: Optional[str] = None
    status_ret_export: Optional[str] = None

    mensagem_ret_export: Optional[bytes] = None
    emolumento_item_id: Optional[int] = None
    numero_selo: Optional[str] = None
    situacao_diferido: Optional[str] = None
    data_inutilizacao: Optional[datetime] = None
    selo_protocolo: Optional[str] = None

    valor_fundo_selo: Optional[Decimal] = None
    inteiro_teor_texto: Optional[bytes] = None
    tipo_envolvido: Optional[str] = None
    idap: Optional[str] = None
    fundo_selo: Optional[int] = None
    distribuidor: Optional[int] = None
    data_importacao: Optional[datetime] = None
    selo_retificado: Optional[str] = None

    class Config:
        from_attributes = True


class GSeloLivroIdSchema(BaseModel):
    selo_livro_id: int


class GSeloLivroLivreSchema(BaseModel):
    selo_grupo_id: int


class GSeloLivroLivreQuantidadeSchema(BaseModel):
    selo_grupo_id: int
    quantidade: int


class GSeloLivroSaveSchema(GSeloLivroSchema):
    pass


class GSeloLivroUpdateSchema(GSeloLivroSchema):
    selo_livro_id: int
