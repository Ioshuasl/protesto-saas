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
    from packages.v1.administrativo.model.g_tb_estadocivil import (
        get_g_tb_estadocivil_model,
    )
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
    from packages.v1.administrativo.model.p_pessoa import get_p_pessoa_model
    from packages.v1.administrativo.model.p_titulo import get_p_titulo_model

    P_BANCO = get_p_banco_model()
    P_ESPECIE = get_p_especie_model()
    P_LIVRO_NATUREZA = get_p_livro_natureza_model()
    P_LIVRO_ANDAMENTO = get_p_livro_andamento_model()
    P_LAYOUT = get_p_layout_model()
    P_PESSOA = get_p_pessoa_model()
    P_TITULO = get_p_titulo_model()
    G_TB_ESTADOCIVIL = get_g_tb_estadocivil_model()
    G_TB_PROFISSAO = get_g_tb_profissao_model()
    G_CIDADE = get_g_cidade_model()

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

    # --- P_ESPECIE ---
    P_ESPECIE.hasMany(
        P_TITULO,
        {"as": "titulos", "foreignKey": "ESPECIE_ID", "sourceKey": "ESPECIE_ID"},
    )
    P_TITULO.belongsTo(
        P_ESPECIE,
        {"as": "especie", "foreignKey": "ESPECIE_ID", "targetKey": "ESPECIE_ID"},
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

    _ASSOCIATIONS_REGISTERED = True
