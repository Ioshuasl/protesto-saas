# Importa o gerenciador de rotas do FastAPI
from fastapi import APIRouter

# Importa os módulos de rotas específicos
from packages.v1.administrativo.endpoints import (
    g_cartorio_endpoint,
    g_feriado_endpoint,
    p_banco_endpoint,
    p_especie_endpoint,
    p_livro_natureza_endpoint,
    p_livro_andamento_endpoint,
    g_emolumento_endpoint,
    g_emolumento_periodo_endpoint,
    g_gramatica_endpoint,
    g_ibge_pais_endpoint,
    g_natureza_titulo_endpoint,
    g_selo_grupo_endpoint,
    g_selo_livro_endpoint,
    t_ato_partetipo_endpoint,
    t_biometria_pessoa_endpoint,
    t_censec_tiponatureza_endpoint,
)
from packages.v1.administrativo.endpoints import (
    g_emolumento_item_endpoint,
    t_censec_tipoato_endpoint,
)
from packages.v1.administrativo.endpoints import t_censec_qualidadeato_endpoint
from packages.v1.administrativo.endpoints import g_tb_txmodelogrupo_endpoint
from packages.v1.administrativo.endpoints import g_tb_profissao_endpoint
from packages.v1.administrativo.endpoints import c_caixa_item_endpoint
from packages.v1.administrativo.endpoints import g_usuario_endpoint
from packages.v1.administrativo.endpoints import c_caixa_servico_endpoint
from packages.v1.administrativo.endpoints import t_tb_sinal_publico_endpoint
from packages.v1.administrativo.endpoints import t_tb_reconhecimentotipo_endpoint
from packages.v1.administrativo.endpoints import t_tb_andamentoservico_endpoint
from packages.v1.administrativo.endpoints import t_tb_cartorio_endpoint
from packages.v1.administrativo.endpoints import g_tb_regimecomunhao_endpoint
from packages.v1.administrativo.endpoints import g_tb_regimebens_endpoint
from packages.v1.administrativo.endpoints import t_censec_endpoint
from packages.v1.administrativo.endpoints import t_censec_naturezalitigio_endpoint
from packages.v1.administrativo.endpoints import t_censec_qualidade_endpoint
from packages.v1.administrativo.endpoints import g_tb_estadocivil_endpoint
from packages.v1.administrativo.endpoints import g_medida_tipo_endpoint
from packages.v1.administrativo.endpoints import t_minuta_endpoint
from packages.v1.administrativo.endpoints import g_tb_documentotipo_endpoint
from packages.v1.administrativo.endpoints import g_natureza_endpoint
from packages.v1.administrativo.endpoints import g_tb_bairro_endpoint
from packages.v1.administrativo.endpoints import g_tb_tipologradouro_endpoint
from packages.v1.administrativo.endpoints import g_cidade_endpoint
from packages.v1.administrativo.endpoints import t_servico_tipo_endpoint
from packages.v1.administrativo.endpoints import t_livro_andamento_endpoint
from packages.v1.administrativo.endpoints import t_livro_natureza_endpoint
from packages.v1.administrativo.endpoints import g_marcacao_tipo_endpoint
from packages.v1.administrativo.endpoints import t_servico_etiqueta_endpoint
from packages.v1.administrativo.endpoints import g_uf_endpoint
from packages.v1.administrativo.endpoints import t_imovel_endpoint
from packages.v1.administrativo.endpoints import t_imovel_unidade_endpoint
from packages.v1.administrativo.endpoints import t_pessoa_endpoint
from packages.v1.administrativo.endpoints import t_pessoa_representante_endpoint
from packages.v1.administrativo.endpoints import t_pessoa_sinal_publico_endpoint
from packages.v1.administrativo.endpoints import g_calculo_endpoint
from packages.v1.docx.endpoints import docx_endpoint
from packages.v1.ged.endpoints import ged_endpoint
from packages.v1.nfse.endpoints import nfse_endpoint
from packages.v1.nfse.endpoints import parametros_endpoint
from packages.v1.parametros.endpoints import g_config_endpoint
from packages.v1.servicos.atos.endpoint import (
    t_ato_andamento_endpoint,
    t_ato_endpoint,
    t_ato_parteimovel_endpoint,
    t_ato_tipo_endpoint,
    t_ato_vinculoimovel_endpoint,
    t_ato_vinculoparte_endpoint,
    t_ato_vinculovalor_endpoint,
    t_historico_endpoint,
)
from packages.v1.servicos.balcao.endpoints import (
    t_pessoa_cartao_endpoint,
    t_servico_itempedido_endpoint,
    t_servico_pedido_endpoint,
)

# Cria uma instância do APIRouter que vai agregar todas as rotas da API
api_router = APIRouter()

# Inclui as rotas de c_caixa_item
api_router.include_router(
    c_caixa_item_endpoint.router,
    prefix="/administrativo/c_caixa_item",
    tags=["Caixa Item"],
)

# Inclui as rotas de g_usuario
api_router.include_router(
    g_usuario_endpoint.router,
    prefix="/administrativo/g_usuario",
    tags=["Gerenciamento de Usuários"],
)

# Inclui as rotas de c_caixa_servico
api_router.include_router(
    c_caixa_servico_endpoint.router,
    prefix="/administrativo/c_caixa_servico",
    tags=["Caixa Serviço"],
)

# Inclui as rotas de t_tb_reconhecimentotipo
api_router.include_router(
    t_tb_sinal_publico_endpoint.router,
    prefix="/administrativo/t_tb_sinal_publico",
    tags=["Sinal publico"],
)

# Inclui as rotas de t_tb_reconhecimentotipo
api_router.include_router(
    t_tb_reconhecimentotipo_endpoint.router,
    prefix="/administrativo/t_tb_reconhecimentotipo",
    tags=["Tipos de reconhecimento"],
)

# Inclui as rotas de t_tb_andamentoservico
api_router.include_router(
    t_tb_andamentoservico_endpoint.router,
    prefix="/administrativo/t_tb_andamentoservico",
    tags=["Andamentos de serviço"],
)

# Inclui as rotas de t_tb_cartorio
api_router.include_router(
    t_tb_cartorio_endpoint.router,
    prefix="/administrativo/t_tb_cartorio",
    tags=["Cartorio"],
)

# Inclui as rotas de g_tb_profissao
api_router.include_router(
    g_tb_profissao_endpoint.router,
    prefix="/administrativo/g_tb_profissao",
    tags=["Profissões"],
)

# Inclui as rotas de g_tb_regimecomunhao
api_router.include_router(
    g_tb_regimecomunhao_endpoint.router,
    prefix="/administrativo/g_tb_regimecomunhao",
    tags=["Regime de Comunhão"],
)

# Inclui as rotas de g_tb_txmodelogrupo
api_router.include_router(
    g_tb_txmodelogrupo_endpoint.router,
    prefix="/administrativo/g_tb_txmodelogrupo",
    tags=["Modelo grupo"],
)

# Inclui as rotas de g_tb_regimebens
api_router.include_router(
    g_tb_regimebens_endpoint.router,
    prefix="/administrativo/g_tb_regimebens",
    tags=["Regime de bens"],
)


# Inclui as rotas de t_censec
api_router.include_router(
    t_censec_endpoint.router,
    prefix="/administrativo/t_censec",
    tags=["Configurações do CENSEC"],
)


# Inclui as rotas de t_censec_naturezalitigio
api_router.include_router(
    t_censec_naturezalitigio_endpoint.router,
    prefix="/administrativo/t_censec_naturezalitigio",
    tags=["CENSEC - Natureza Litígio"],
)


# Inclui as rotas de t_censec_qualidade
api_router.include_router(
    t_censec_qualidade_endpoint.router,
    prefix="/administrativo/t_censec_qualidade",
    tags=["CENSEC - Qualidade"],
)

# Inclui as rotas de g_tb_estadocivil
api_router.include_router(
    g_tb_estadocivil_endpoint.router,
    prefix="/administrativo/g_tb_estadocivil",
    tags=["Estado Civil"],
)

# Inclui as rotas de g_tg_medida_tipob_estadocivil
api_router.include_router(
    g_medida_tipo_endpoint.router,
    prefix="/administrativo/g_medida_tipo",
    tags=["Tipo de Medidas"],
)

# Inclui as rotas de g_tg_medida_tipob_estadocivil
api_router.include_router(
    t_minuta_endpoint.router,
    prefix="/administrativo/t_minuta",
    tags=["Gerenciamento de Minutas"],
)

# Inclui as rotas de g_tb_documentotipo
api_router.include_router(
    g_tb_documentotipo_endpoint.router,
    prefix="/administrativo/g_tb_documentotipo",
    tags=["Documento tipo"],
)

# Inclui as rotas de g_natureza
api_router.include_router(
    g_natureza_endpoint.router,
    prefix="/administrativo/g_natureza",
    tags=["Gerenciamento de Naturezas do Ato"],
)


# Inclui as rotas de t_censec_naturezalitigio
api_router.include_router(
    g_tb_bairro_endpoint.router,
    prefix="/administrativo/g_tb_bairro",
    tags=["CENSEC - Bairro"],
)

# Inclui as rotas de g_tb_tipologradouro
api_router.include_router(
    g_tb_tipologradouro_endpoint.router,
    prefix="/administrativo/g_tb_tipologradouro",
    tags=["Tipo logradouro"],
)

# Inclui as rotas de g_cidade
api_router.include_router(
    g_cidade_endpoint.router,
    prefix="/administrativo/g_cidade",
    tags=["Gerenciamento de Cidades"],
)

# Inclui as rotas de t_servico_tipo
api_router.include_router(
    t_servico_tipo_endpoint.router,
    prefix="/administrativo/t_servico_tipo",
    tags=["Serviço tipo"],
)

# Inclui as rotas de g_marcacao_tipo
api_router.include_router(
    g_marcacao_tipo_endpoint.router,
    prefix="/administrativo/g_marcacao_tipo",
    tags=["Marcação tipo"],
)

# Inclui as rotas de g_marcacao_tipo
api_router.include_router(
    t_servico_etiqueta_endpoint.router,
    prefix="/administrativo/t_servico_etiqueta",
    tags=["Serviço etiqueta"],
)

# Inclui as rotas de g_uf
api_router.include_router(
    g_uf_endpoint.router,
    prefix="/administrativo/g_uf",
    tags=["Gerenciamento de Estados"],
)

# Inclui as rotas de t_imovel
api_router.include_router(
    t_imovel_endpoint.router,
    prefix="/administrativo/t_imovel",
    tags=["Gerenciamento de Imóveis"],
)

# Inclui as rotas de t_imovel_unidade
api_router.include_router(
    t_imovel_unidade_endpoint.router,
    prefix="/administrativo/t_imovel_unidade",
    tags=["Imóveis Unidades"],
)

# Inclui as rotas de t_pessoa
api_router.include_router(
    t_pessoa_endpoint.router,
    prefix="/administrativo/t_pessoa",
    tags=["Pessoas Fisicas e Jurídicas"],
)

# Inclui as rotas de t_pessoa_representante
api_router.include_router(
    t_pessoa_representante_endpoint.router,
    prefix="/administrativo/t_pessoa_representante",
    tags=["Representante de pessoas jurídicas"],
)

# Inclui as rotas de t_pessoa_sinal_publico
api_router.include_router(
    t_pessoa_sinal_publico_endpoint.router,
    prefix="/administrativo/t_pessoa_sinal_publico",
    tags=["Sinal publico por pessoa"],
)

# Inclui as rotas de t_censec_tipoato
api_router.include_router(
    t_censec_tipoato_endpoint.router,
    prefix="/administrativo/t_censec_tipoato",
    tags=["CENSEC Tipo atos"],
)

# Inclui as rotas de t_censec_qualidadeato
api_router.include_router(
    t_censec_qualidadeato_endpoint.router,
    prefix="/administrativo/t_censec_qualidadeato",
    tags=["CENSEC Qualidade Ato"],
)

# Inclui as rotas de t_ato_partetipo
api_router.include_router(
    t_ato_partetipo_endpoint.router,
    prefix="/administrativo/t_ato_partetipo",
    tags=["Tipo de Parte do Ato"],
)

# Inclui as rotas de t_censec_tiponatureza
api_router.include_router(
    t_censec_tiponatureza_endpoint.router,
    prefix="/administrativo/t_censec_tiponatureza",
    tags=["Tipo de Natureza do CENSEC"],
)

# Inclui as rotas de g_natureza_titulo
api_router.include_router(
    g_natureza_titulo_endpoint.router,
    prefix="/administrativo/g_natureza_titulo",
    tags=["Títulos do GNatureza"],
)

# Inclui as rotas de g_gramatica
api_router.include_router(
    g_gramatica_endpoint.router,
    prefix="/administrativo/g_gramatica",
    tags=["Dicionário Gramatical"],
)

# Inclui as rotas de g_cartorio
api_router.include_router(
    g_cartorio_endpoint.router,
    prefix="/administrativo/g_cartorio",
    tags=["Dados do Cartório"],
)

# Inclui as rotas de g_feriado
api_router.include_router(
    g_feriado_endpoint.router,
    prefix="/administrativo/g_feriado",
    tags=["Feriados"],
)

# Inclui as rotas de p_banco
api_router.include_router(
    p_banco_endpoint.router,
    prefix="/administrativo/p_banco",
    tags=["Bancos"],
)

# Inclui as rotas de p_especie
api_router.include_router(
    p_especie_endpoint.router,
    prefix="/administrativo/p_especie",
    tags=["Especies"],
)

# Inclui as rotas de p_livro_natureza
api_router.include_router(
    p_livro_natureza_endpoint.router,
    prefix="/administrativo/p_livro_natureza",
    tags=["Livros de natureza"],
)

# Inclui as rotas de p_livro_andamento
api_router.include_router(
    p_livro_andamento_endpoint.router,
    prefix="/administrativo/p_livro_andamento",
    tags=["Livros de andamento"],
)

# Inclui as rotas de g_emolumento
api_router.include_router(
    g_emolumento_endpoint.router,
    prefix="/administrativo/g_emolumento",
    tags=["Emolumentos"],
)

# Inclui as rotas de g_emolumento_item
api_router.include_router(
    g_emolumento_item_endpoint.router,
    prefix="/administrativo/g_emolumento_item",
    tags=["Emolumento Item"],
)

# Inclui as rotas de g_emolumento periodo
api_router.include_router(
    g_emolumento_periodo_endpoint.router,
    prefix="/administrativo/g_emolumento_periodo",
    tags=["Periodos de Emolumentos"],
)

# Inclui as rotas de g_emolumento periodo
api_router.include_router(
    g_selo_grupo_endpoint.router,
    prefix="/administrativo/g_selo_grupo",
    tags=["Grupos de Selos"],
)

# Inclui as rotas de g_emolumento periodo
api_router.include_router(
    g_calculo_endpoint.router,
    prefix="/administrativo/g_calculo",
    tags=["Calculo Rápido"],
)

# Inclui as rotas de g_emolumento periodo
api_router.include_router(
    g_emolumento_item_endpoint.router,
    prefix="/administrativo/g_emolumento_item",
    tags=["Itens do Emolumento"],
)

# Inclui as rotas de g_emolumento periodo
api_router.include_router(
    t_servico_pedido_endpoint.router,
    prefix="/servicos/pedidos/t_servico_pedido",
    tags=["Pedido"],
)

# Inclui as rotas de g_emolumento periodo
api_router.include_router(
    t_servico_itempedido_endpoint.router,
    prefix="/servicos/pedidos/t_servico_itempedido",
    tags=["Itens do Pedido"],
)


# Inclui as rotas de g_emolumento periodo
api_router.include_router(
    t_pessoa_cartao_endpoint.router,
    prefix="/servicos/pedidos/t_pessoa_cartao",
    tags=["Pessoa Cartao"],
)

# Inclui as rotas de g_emolumento periodo
api_router.include_router(
    t_ato_endpoint.router,
    prefix="/servicos/atos/t_ato",
    tags=["Atos"],
)

# Inclui as rotas de g_emolumento periodo
api_router.include_router(
    t_ato_vinculoparte_endpoint.router,
    prefix="/servicos/atos/t_ato_vinculoparte",
    tags=["Atos Vinculo Parte"],
)

# Inclui as rotas de g_emolumento periodo
api_router.include_router(
    t_ato_vinculovalor_endpoint.router,
    prefix="/servicos/atos/t_ato_vinculovalor",
    tags=["Atos Vinculo Valor"],
)

# Inclui as rotas de g_emolumento periodo
api_router.include_router(
    t_ato_vinculoimovel_endpoint.router,
    prefix="/servicos/atos/t_ato_vinculoimovel",
    tags=["Atos Vinculo Valor"],
)

# Inclui as rotas de g_emolumento periodo
api_router.include_router(
    t_ato_andamento_endpoint.router,
    prefix="/servicos/atos/t_ato_andamento",
    tags=["Atos Vinculo Valor"],
)

# Inclui as rotas de g_emolumento periodo
api_router.include_router(
    t_ato_parteimovel_endpoint.router,
    prefix="/servicos/atos/t_ato_parteimovel",
    tags=["Atos Vinculo Valor"],
)

# Inclui as rotas de g_emolumento periodo
api_router.include_router(
    t_ato_tipo_endpoint.router,
    prefix="/servicos/atos/t_ato_tipo",
    tags=["Atos Vinculo Valor"],
)

# Inclui as rotas de g_emolumento periodo
api_router.include_router(
    t_historico_endpoint.router,
    prefix="/servicos/t_historico",
    tags=["Historicos de serviços"],
)


# Inclui as rotas de g_emolumento periodo
api_router.include_router(
    t_biometria_pessoa_endpoint.router,
    prefix="/administrativo/t_biometria_pessoa",
    tags=["Pessoa Cartao"],
)

# Inclui as rotas de g_emolumento periodo
api_router.include_router(
    g_selo_livro_endpoint.router,
    prefix="/administrativo/g_selo_livro",
    tags=["Selos Livro"],
)

# Inclui as rotas de t_livro_natureza
api_router.include_router(
    t_livro_natureza_endpoint.router,
    prefix="/administrativo/t_livro_natureza",
    tags=["Livro Natureza"],
)

# Inclui as rotas de t_livro_andamento
api_router.include_router(
    t_livro_andamento_endpoint.router,
    prefix="/administrativo/t_livro_andamento",
    tags=["Livro Andamento"],
)

# Inclui as rotas de g_emolumento periodo
api_router.include_router(
    ged_endpoint.router,
    prefix="/ged",
    tags=["Selos Livro"],
)


# Inclui as rotas de docx
api_router.include_router(
    docx_endpoint.router,
    prefix="/administrativo/docx",
    tags=["Docx"],
)


# Inclui as rotas de docx
api_router.include_router(
    g_ibge_pais_endpoint.router,
    prefix="/administrativo/g_ibge_pais",
    tags=["Países"],
)

# Inclui as rotas de NFS-e
api_router.include_router(
    nfse_endpoint.router,
    prefix="/nfse",
    tags=["NFS-e"],
)

# Inclui as rotas de Parametros NFS-e
api_router.include_router(
    parametros_endpoint.router,
    prefix="/nfse/parametros",
    tags=["NFS-e Parametros"],
)

# Inclui as rotas de Parametros G_CONFIG
api_router.include_router(
    g_config_endpoint.router,
    prefix="/parametros/g_config",
    tags=["Parametros G_CONFIG"],
)
