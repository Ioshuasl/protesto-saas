"""
Associações ORM do pacote administrativo.

Ordem: todos os model/*.py definidos antes de chamar register_administrativo_associations().
Sintaxe: docs/orm-firebird-py/README.md (seção Associações).
"""

from __future__ import annotations

_ASSOCIATIONS_REGISTERED = False


def register_administrativo_associations() -> None:
    global _ASSOCIATIONS_REGISTERED
    if _ASSOCIATIONS_REGISTERED:
        return

    from packages.v1.administrativo.model.g_cidade import get_g_cidade_model
    from packages.v1.administrativo.model.g_selo_grupo import get_g_selo_grupo_model
    from packages.v1.administrativo.model.g_selo_livro import get_g_selo_livro_model
    from packages.v1.administrativo.model.g_selo_lote import get_g_selo_lote_model
    from packages.v1.administrativo.model.g_emolumento import get_g_emolumento_model
    from packages.v1.administrativo.model.g_emolumento_item import (
        get_g_emolumento_item_model,
    )
    from packages.v1.administrativo.model.g_emolumento_periodo import (
        get_g_emolumento_periodo_model,
    )
    from packages.v1.administrativo.model.g_sistema import get_g_sistema_model
    from packages.v1.administrativo.model.g_tb_estadocivil import (
        get_g_tb_estadocivil_model,
    )
    from packages.v1.administrativo.model.g_usuario import get_g_usuario_model
    from packages.v1.administrativo.model.g_tb_profissao import get_g_tb_profissao_model
    from packages.v1.administrativo.model.p_banco import get_p_banco_model
    from packages.v1.administrativo.model.p_especie import get_p_especie_model
    from packages.v1.administrativo.model.p_livro_andamento import (
        get_p_livro_andamento_model,
    )
    from packages.v1.administrativo.model.p_livro_natureza import (
        get_p_livro_natureza_model,
    )
    from packages.v1.administrativo.model.p_layout import get_p_layout_model
    from packages.v1.administrativo.model.p_motivos import get_p_motivos_model
    from packages.v1.administrativo.model.p_andamento import get_p_andamento_model
    from packages.v1.administrativo.model.p_motivos_cancelamento import (
        get_p_motivos_cancelamento_model,
    )
    from packages.v1.administrativo.model.p_ocorrencia_andamento import (
        get_p_ocorrencia_andamento_model,
    )
    from packages.v1.administrativo.model.p_ocorrencias import get_p_ocorrencias_model
    from packages.v1.administrativo.model.p_pessoa import get_p_pessoa_model
    from packages.v1.administrativo.model.p_pessoa_vinculo import (
        get_p_pessoa_vinculo_model,
    )
    from packages.v1.administrativo.model.p_certidao import get_p_certidao_model
    from packages.v1.administrativo.model.p_titulo import get_p_titulo_model

    P_BANCO = get_p_banco_model()
    P_ESPECIE = get_p_especie_model()
    P_LIVRO_NATUREZA = get_p_livro_natureza_model()
    P_LIVRO_ANDAMENTO = get_p_livro_andamento_model()
    P_LAYOUT = get_p_layout_model()
    P_MOTIVOS = get_p_motivos_model()
    P_MOTIVOS_CANCELAMENTO = get_p_motivos_cancelamento_model()
    P_ANDAMENTO = get_p_andamento_model()
    P_OCORRENCIA_ANDAMENTO = get_p_ocorrencia_andamento_model()
    P_OCORRENCIAS = get_p_ocorrencias_model()
    P_PESSOA = get_p_pessoa_model()
    P_PESSOA_VINCULO = get_p_pessoa_vinculo_model()
    P_CERTIDAO = get_p_certidao_model()
    P_TITULO = get_p_titulo_model()
    G_TB_ESTADOCIVIL = get_g_tb_estadocivil_model()
    G_TB_PROFISSAO = get_g_tb_profissao_model()
    G_CIDADE = get_g_cidade_model()
    G_USUARIO = get_g_usuario_model()
    G_SELO_GRUPO = get_g_selo_grupo_model()
    G_SELO_LOTE = get_g_selo_lote_model()
    G_SELO_LIVRO = get_g_selo_livro_model()
    G_EMOLUMENTO = get_g_emolumento_model()
    G_EMOLUMENTO_ITEM = get_g_emolumento_item_model()
    G_EMOLUMENTO_PERIODO = get_g_emolumento_periodo_model()
    G_SISTEMA = get_g_sistema_model()

    # --- P_BANCO ---
    P_BANCO.belongsTo(
        P_LAYOUT,
        {"as": "layout", "foreignKey": "LAYOUT_ID", "targetKey": "LAYOUT_ID"},
    )
    P_BANCO.belongsTo(
        P_PESSOA,
        {"as": "pessoa", "foreignKey": "PESSOA_ID", "targetKey": "PESSOA_ID"},
    )
    P_BANCO.hasMany(
        P_TITULO,
        {"as": "titulos", "foreignKey": "BANCO_ID", "sourceKey": "BANCO_ID"},
    )
    P_TITULO.belongsTo(
        P_BANCO,
        {"as": "banco", "foreignKey": "BANCO_ID", "targetKey": "BANCO_ID"},
    )

    # --- P_ESPECIE ---
    P_ESPECIE.hasMany(
        P_TITULO,
        {"as": "titulos", "foreignKey": "ESPECIE_ID", "sourceKey": "ESPECIE_ID"},
    )
    P_TITULO.belongsTo(
        P_ESPECIE,
        {"as": "especie", "foreignKey": "ESPECIE_ID", "targetKey": "ESPECIE_ID"},
    )
    P_TITULO.belongsTo(
        P_MOTIVOS,
        {
            "as": "motivo_apontamento",
            "foreignKey": "MOTIVO_APONTAMENTO_ID",
            "targetKey": "MOTIVOS_ID",
        },
    )
    P_MOTIVOS.hasMany(
        P_TITULO,
        {
            "as": "titulos",
            "foreignKey": "MOTIVO_APONTAMENTO_ID",
            "sourceKey": "MOTIVOS_ID",
        },
    )

    # --- P_MOTIVOS_CANCELAMENTO ---
    P_MOTIVOS_CANCELAMENTO.hasMany(
        P_TITULO,
        {
            "as": "titulos",
            "foreignKey": "MOTIVO_CANCELAMENTO",
            "sourceKey": "MOTIVOS_CANCELAMENTO_ID",
        },
    )
    P_TITULO.belongsTo(
        P_MOTIVOS_CANCELAMENTO,
        {
            "as": "motivo_cancelamento",
            "foreignKey": "MOTIVO_CANCELAMENTO",
            "targetKey": "MOTIVOS_CANCELAMENTO_ID",
        },
    )

    # --- P_OCORRENCIAS / P_TITULO ---
    P_OCORRENCIAS.hasMany(
        P_TITULO,
        {
            "as": "titulos",
            "foreignKey": "OCORRENCIA_ID",
            "sourceKey": "OCORRENCIAS_ID",
        },
    )
    P_TITULO.belongsTo(
        P_OCORRENCIAS,
        {
            "as": "ocorrencia",
            "foreignKey": "OCORRENCIA_ID",
            "targetKey": "OCORRENCIAS_ID",
        },
    )

    # --- P_OCORRENCIA_ANDAMENTO / P_TITULO / P_ANDAMENTO ---
    P_OCORRENCIA_ANDAMENTO.hasMany(
        P_TITULO,
        {
            "as": "titulos",
            "foreignKey": "OCORRENCIA_ANDAMENTO_ID",
            "sourceKey": "OCORRENCIA_ANDAMENTO_ID",
        },
    )
    P_TITULO.belongsTo(
        P_OCORRENCIA_ANDAMENTO,
        {
            "as": "ocorrencia_andamento",
            "foreignKey": "OCORRENCIA_ANDAMENTO_ID",
            "targetKey": "OCORRENCIA_ANDAMENTO_ID",
        },
    )
    P_OCORRENCIA_ANDAMENTO.hasMany(
        P_ANDAMENTO,
        {
            "as": "andamentos",
            "foreignKey": "OCORRENCIA_ANDAMENTO_ID",
            "sourceKey": "OCORRENCIA_ANDAMENTO_ID",
        },
    )
    P_ANDAMENTO.belongsTo(
        P_OCORRENCIA_ANDAMENTO,
        {
            "as": "ocorrencia_andamento",
            "foreignKey": "OCORRENCIA_ANDAMENTO_ID",
            "targetKey": "OCORRENCIA_ANDAMENTO_ID",
        },
    )
    P_TITULO.hasMany(
        P_ANDAMENTO,
        {
            "as": "andamentos",
            "foreignKey": "TITULO_ID",
            "sourceKey": "TITULO_ID",
        },
    )
    P_ANDAMENTO.belongsTo(
        P_TITULO,
        {"as": "titulo", "foreignKey": "TITULO_ID", "targetKey": "TITULO_ID"},
    )

    # --- P_LIVRO_NATUREZA / P_LIVRO_ANDAMENTO ---
    P_LIVRO_NATUREZA.hasMany(
        P_LIVRO_ANDAMENTO,
        {
            "as": "livros_andamento",
            "foreignKey": "LIVRO_NATUREZA_ID",
            "sourceKey": "LIVRO_NATUREZA_ID",
        },
    )
    P_LIVRO_ANDAMENTO.belongsTo(
        P_LIVRO_NATUREZA,
        {
            "as": "livro_natureza",
            "foreignKey": "LIVRO_NATUREZA_ID",
            "targetKey": "LIVRO_NATUREZA_ID",
        },
    )

    # --- P_PESSOA -> tabelas de domínio (N:1 — FK em P_PESSOA) ---
    P_PESSOA.belongsTo(
        G_TB_ESTADOCIVIL,
        {
            "as": "estado_civil",
            "foreignKey": "ESTADO_CIVIL_ID",
            "targetKey": "TB_ESTADOCIVIL_ID",
        },
    )
    P_PESSOA.belongsTo(
        G_TB_PROFISSAO,
        {
            "as": "profissao",
            "foreignKey": "PROFISSAO_ID",
            "targetKey": "TB_PROFISSAO_ID",
        },
    )
    P_PESSOA.belongsTo(
        G_CIDADE,
        {"as": "cidade", "foreignKey": "CIDADE_ID", "targetKey": "CIDADE_ID"},
    )

    # --- inversas 1:N (opcional para include a partir do domínio) ---
    G_TB_ESTADOCIVIL.hasMany(
        P_PESSOA,
        {
            "as": "pessoas",
            "foreignKey": "ESTADO_CIVIL_ID",
            "sourceKey": "TB_ESTADOCIVIL_ID",
        },
    )
    G_TB_PROFISSAO.hasMany(
        P_PESSOA,
        {
            "as": "pessoas",
            "foreignKey": "PROFISSAO_ID",
            "sourceKey": "TB_PROFISSAO_ID",
        },
    )
    G_CIDADE.hasMany(
        P_PESSOA,
        {
            "as": "pessoas",
            "foreignKey": "CIDADE_ID",
            "sourceKey": "CIDADE_ID",
        },
    )

    # --- P_PESSOA / P_PESSOA_VINCULO ---
    P_PESSOA.hasMany(
        P_PESSOA_VINCULO,
        {
            "as": "vinculos",
            "foreignKey": "PESSOA_ID",
            "sourceKey": "PESSOA_ID",
        },
    )
    P_PESSOA_VINCULO.belongsTo(
        P_PESSOA,
        {"as": "pessoa", "foreignKey": "PESSOA_ID", "targetKey": "PESSOA_ID"},
    )
    P_PESSOA_VINCULO.belongsTo(
        P_TITULO,
        {"as": "titulo", "foreignKey": "TITULO_ID", "targetKey": "TITULO_ID"},
    )
    P_TITULO.hasMany(
        P_PESSOA_VINCULO,
        {
            "as": "pessoa_vinculos",
            "foreignKey": "TITULO_ID",
            "sourceKey": "TITULO_ID",
        },
    )
    P_PESSOA_VINCULO.belongsTo(
        G_TB_ESTADOCIVIL,
        {
            "as": "estado_civil",
            "foreignKey": "ESTADO_CIVIL_ID",
            "targetKey": "TB_ESTADOCIVIL_ID",
        },
    )
    P_PESSOA_VINCULO.belongsTo(
        G_TB_PROFISSAO,
        {
            "as": "profissao",
            "foreignKey": "PROFISSAO_ID",
            "targetKey": "TB_PROFISSAO_ID",
        },
    )

    # --- G_SELO_GRUPO (auto-referência) ---
    G_SELO_GRUPO.belongsTo(
        G_SELO_GRUPO,
        {
            "as": "grupo_principal",
            "foreignKey": "SELO_GRUPO_ID_PRINCIPAL",
            "targetKey": "SELO_GRUPO_ID",
        },
    )
    G_SELO_GRUPO.belongsTo(
        G_SELO_GRUPO,
        {
            "as": "grupo_agrupador",
            "foreignKey": "SELO_GRUPO_ID_AGRUPADOR",
            "targetKey": "SELO_GRUPO_ID",
        },
    )

    # --- G_SELO_GRUPO / G_SELO_LOTE / G_SELO_LIVRO ---
    G_SELO_GRUPO.hasMany(
        G_SELO_LOTE,
        {
            "as": "lotes",
            "foreignKey": "SELO_GRUPO_ID",
            "sourceKey": "SELO_GRUPO_ID",
        },
    )
    G_SELO_LOTE.belongsTo(
        G_SELO_GRUPO,
        {
            "as": "grupo",
            "foreignKey": "SELO_GRUPO_ID",
            "targetKey": "SELO_GRUPO_ID",
        },
    )
    G_SELO_LOTE.hasMany(
        G_SELO_LIVRO,
        {
            "as": "selos_livro",
            "foreignKey": "SELO_LOTE_ID",
            "sourceKey": "SELO_LOTE_ID",
        },
    )
    G_SELO_LIVRO.belongsTo(
        G_SELO_LOTE,
        {
            "as": "lote",
            "foreignKey": "SELO_LOTE_ID",
            "targetKey": "SELO_LOTE_ID",
        },
    )

    # --- G_EMOLUMENTO / G_EMOLUMENTO_ITEM ---
    G_EMOLUMENTO.hasMany(
        G_EMOLUMENTO_ITEM,
        {
            "as": "itens",
            "foreignKey": "EMOLUMENTO_ID",
            "sourceKey": "EMOLUMENTO_ID",
        },
    )
    G_EMOLUMENTO_ITEM.belongsTo(
        G_EMOLUMENTO,
        {
            "as": "emolumento",
            "foreignKey": "EMOLUMENTO_ID",
            "targetKey": "EMOLUMENTO_ID",
        },
    )
    G_EMOLUMENTO_PERIODO.hasMany(
        G_EMOLUMENTO_ITEM,
        {
            "as": "itens",
            "foreignKey": "EMOLUMENTO_PERIODO_ID",
            "sourceKey": "EMOLUMENTO_PERIODO_ID",
        },
    )
    G_EMOLUMENTO_ITEM.belongsTo(
        G_EMOLUMENTO_PERIODO,
        {
            "as": "emolumento_periodo",
            "foreignKey": "EMOLUMENTO_PERIODO_ID",
            "targetKey": "EMOLUMENTO_PERIODO_ID",
        },
    )

    # --- G_SELO_GRUPO / G_EMOLUMENTO_ITEM ---
    G_SELO_GRUPO.hasMany(
        G_EMOLUMENTO_ITEM,
        {
            "as": "emolumento_itens",
            "foreignKey": "SELO_GRUPO_ID",
            "sourceKey": "SELO_GRUPO_ID",
        },
    )
    G_EMOLUMENTO_ITEM.belongsTo(
        G_SELO_GRUPO,
        {
            "as": "selo_grupo",
            "foreignKey": "SELO_GRUPO_ID",
            "targetKey": "SELO_GRUPO_ID",
        },
    )
    G_EMOLUMENTO_ITEM.hasMany(
        G_SELO_LIVRO,
        {
            "as": "selos_livro",
            "foreignKey": "EMOLUMENTO_ITEM_ID",
            "sourceKey": "EMOLUMENTO_ITEM_ID",
        },
    )
    G_SELO_LIVRO.belongsTo(
        G_EMOLUMENTO_ITEM,
        {
            "as": "emolumento_item",
            "foreignKey": "EMOLUMENTO_ITEM_ID",
            "targetKey": "EMOLUMENTO_ITEM_ID",
        },
    )

    # --- G_SISTEMA / G_EMOLUMENTO (associação lógica por coluna SISTEMA_ID) ---
    G_SISTEMA.hasMany(
        G_EMOLUMENTO,
        {"as": "emolumentos", "foreignKey": "SISTEMA_ID", "sourceKey": "SISTEMA_ID"},
    )
    G_EMOLUMENTO.belongsTo(
        G_SISTEMA,
        {"as": "sistema", "foreignKey": "SISTEMA_ID", "targetKey": "SISTEMA_ID"},
    )

    # --- G_USUARIO / G_SELO_LIVRO ---
    G_USUARIO.hasMany(
        G_SELO_LIVRO,
        {
            "as": "selos_livro",
            "foreignKey": "USUARIO_ID",
            "sourceKey": "USUARIO_ID",
        },
    )
    G_SELO_LIVRO.belongsTo(
        G_USUARIO,
        {
            "as": "usuario",
            "foreignKey": "USUARIO_ID",
            "targetKey": "USUARIO_ID",
        },
    )
    G_USUARIO.hasMany(
        G_SELO_LIVRO,
        {
            "as": "selos_livro_exportacao",
            "foreignKey": "USUARIO_ID_EXPORTACAO",
            "sourceKey": "USUARIO_ID",
        },
    )
    G_SELO_LIVRO.belongsTo(
        G_USUARIO,
        {
            "as": "usuario_exportacao",
            "foreignKey": "USUARIO_ID_EXPORTACAO",
            "targetKey": "USUARIO_ID",
        },
    )

    # --- G_USUARIO / P_ANDAMENTO / P_LIVRO_ANDAMENTO ---
    G_USUARIO.hasMany(
        P_ANDAMENTO,
        {
            "as": "andamentos",
            "foreignKey": "USUARIO_ID",
            "sourceKey": "USUARIO_ID",
        },
    )
    P_ANDAMENTO.belongsTo(
        G_USUARIO,
        {
            "as": "usuario",
            "foreignKey": "USUARIO_ID",
            "targetKey": "USUARIO_ID",
        },
    )
    G_USUARIO.hasMany(
        P_LIVRO_ANDAMENTO,
        {
            "as": "livros_andamento",
            "foreignKey": "USUARIO_ID",
            "sourceKey": "USUARIO_ID",
        },
    )
    P_LIVRO_ANDAMENTO.belongsTo(
        G_USUARIO,
        {
            "as": "usuario",
            "foreignKey": "USUARIO_ID",
            "targetKey": "USUARIO_ID",
        },
    )

    # --- G_USUARIO / P_TITULO (assinaturas) ---
    G_USUARIO.hasMany(
        P_TITULO,
        {
            "as": "titulos_assina_prot",
            "foreignKey": "USER_ASSINA_PROT",
            "sourceKey": "USUARIO_ID",
        },
    )
    P_TITULO.belongsTo(
        G_USUARIO,
        {
            "as": "usuario_assina_prot",
            "foreignKey": "USER_ASSINA_PROT",
            "targetKey": "USUARIO_ID",
        },
    )
    G_USUARIO.hasMany(
        P_TITULO,
        {
            "as": "titulos_assina_apont",
            "foreignKey": "USER_ASSINA_APONT",
            "sourceKey": "USUARIO_ID",
        },
    )
    P_TITULO.belongsTo(
        G_USUARIO,
        {
            "as": "usuario_assina_apont",
            "foreignKey": "USER_ASSINA_APONT",
            "targetKey": "USUARIO_ID",
        },
    )

    # --- G_USUARIO / P_CERTIDAO ---
    G_USUARIO.hasMany(
        P_CERTIDAO,
        {
            "as": "certidoes",
            "foreignKey": "USUARIO_ID",
            "sourceKey": "USUARIO_ID",
        },
    )
    P_CERTIDAO.belongsTo(
        G_USUARIO,
        {
            "as": "usuario",
            "foreignKey": "USUARIO_ID",
            "targetKey": "USUARIO_ID",
        },
    )

    _ASSOCIATIONS_REGISTERED = True
