from pydantic import BaseModel
from typing import Optional

# ----------------------------------------------------
# Schema base - representa a tabela G_NATUREZA_TITULO
# ----------------------------------------------------
class GNaturezaTituloSchema(BaseModel):
    codigo_natureza_sef: Optional[float] = None
    emolumento_id: Optional[float] = None
    natureza_titulo_id: Optional[int] = None
    descricao: Optional[str] = None
    prazo: Optional[float] = None
    situacao: Optional[str] = None
    abrir_matricula: Optional[str] = None
    sistema_id: Optional[float] = None
    codigo_doi: Optional[float] = None
    tipo_cobranca: Optional[str] = None
    tipo_titulo: Optional[str] = None
    possui_valor: Optional[str] = None
    pertence_registro_imovel: Optional[str] = None
    emitir_etiqueta: Optional[str] = None
    tipo_onus: Optional[str] = None
    prazo_tipo: Optional[str] = None
    utilizar_desconto: Optional[str] = None
    desconto: Optional[float] = None
    prazo_especial: Optional[str] = None
    informar_doi: Optional[str] = None
    usar_lancar_itens_automaticos: Optional[str] = None
    nao_gerar_selo: Optional[str] = None
    quantidade_busca: Optional[float] = None
    quantidade_folha_excedente: Optional[float] = None
    tipo_recibo: Optional[str] = None
    template_id: Optional[float] = None
    template_id_positiva: Optional[float] = None
    editar_quantidade: Optional[str] = None
    eri_escritura_natureza_id: Optional[float] = None
    selar_na_prenotacao: Optional[str] = None
    texto_certidao: Optional[str] = None
    consolidacao: Optional[str] = None
    nao_cancelar_automatico: Optional[str] = None
    acao_to: Optional[str] = None
    descricao_sinter: Optional[str] = None
    categoria_ato: Optional[str] = None
    nao_gerar_cert_automaticamente: Optional[str] = None
    tipo_operacao: Optional[str] = None
    eh_onr: Optional[str] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema de indexação/listagem (ex: GET /index)
# ----------------------------------------------------
class GNaturezaTituloIndexSchema(BaseModel):
    sistema_id: Optional[int] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um registro pelo ID (GET /{id})
# ----------------------------------------------------
class GNaturezaTituloIdSchema(BaseModel):
    natureza_titulo_id: float

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para criação (POST)
# ----------------------------------------------------
class GNaturezaTituloSaveSchema(BaseModel):
    natureza_titulo_id: Optional[float] = None
    codigo_natureza_sef: Optional[float] = None
    emolumento_id: Optional[float] = None
    descricao: Optional[str] = None
    prazo: Optional[float] = None
    situacao: Optional[str] = None
    abrir_matricula: Optional[str] = None
    sistema_id: Optional[float] = None
    codigo_doi: Optional[float] = None
    tipo_cobranca: Optional[str] = None
    tipo_titulo: Optional[str] = None
    possui_valor: Optional[str] = None
    pertence_registro_imovel: Optional[str] = None
    emitir_etiqueta: Optional[str] = None
    tipo_onus: Optional[str] = None
    prazo_tipo: Optional[str] = None
    utilizar_desconto: Optional[str] = None
    desconto: Optional[float] = None
    prazo_especial: Optional[str] = None
    informar_doi: Optional[str] = None
    usar_lancar_itens_automaticos: Optional[str] = None
    nao_gerar_selo: Optional[str] = None
    quantidade_busca: Optional[float] = None
    quantidade_folha_excedente: Optional[float] = None
    tipo_recibo: Optional[str] = None
    template_id: Optional[float] = None
    template_id_positiva: Optional[float] = None
    editar_quantidade: Optional[str] = None
    eri_escritura_natureza_id: Optional[float] = None
    selar_na_prenotacao: Optional[str] = None
    texto_certidao: Optional[str] = None
    consolidacao: Optional[str] = None
    nao_cancelar_automatico: Optional[str] = None
    acao_to: Optional[str] = None
    descricao_sinter: Optional[str] = None
    categoria_ato: Optional[str] = None
    nao_gerar_cert_automaticamente: Optional[str] = None
    tipo_operacao: Optional[str] = None
    eh_onr: Optional[str] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para atualização (PUT)
# ----------------------------------------------------
class GNaturezaTituloUpdateSchema(BaseModel):
    natureza_titulo_id: Optional[float] = None
    codigo_natureza_sef: Optional[float] = None
    emolumento_id: Optional[float] = None
    descricao: Optional[str] = None
    prazo: Optional[float] = None
    situacao: Optional[str] = None
    abrir_matricula: Optional[str] = None
    sistema_id: Optional[float] = None
    codigo_doi: Optional[float] = None
    tipo_cobranca: Optional[str] = None
    tipo_titulo: Optional[str] = None
    possui_valor: Optional[str] = None
    pertence_registro_imovel: Optional[str] = None
    emitir_etiqueta: Optional[str] = None
    tipo_onus: Optional[str] = None
    prazo_tipo: Optional[str] = None
    utilizar_desconto: Optional[str] = None
    desconto: Optional[float] = None
    prazo_especial: Optional[str] = None
    informar_doi: Optional[str] = None
    usar_lancar_itens_automaticos: Optional[str] = None
    nao_gerar_selo: Optional[str] = None
    quantidade_busca: Optional[float] = None
    quantidade_folha_excedente: Optional[float] = None
    tipo_recibo: Optional[str] = None
    template_id: Optional[float] = None
    template_id_positiva: Optional[float] = None
    editar_quantidade: Optional[str] = None
    eri_escritura_natureza_id: Optional[float] = None
    selar_na_prenotacao: Optional[str] = None
    texto_certidao: Optional[str] = None
    consolidacao: Optional[str] = None
    nao_cancelar_automatico: Optional[str] = None
    acao_to: Optional[str] = None
    descricao_sinter: Optional[str] = None
    categoria_ato: Optional[str] = None
    nao_gerar_cert_automaticamente: Optional[str] = None
    tipo_operacao: Optional[str] = None
    eh_onr: Optional[str] = None

    class Config:
        from_attributes = True
