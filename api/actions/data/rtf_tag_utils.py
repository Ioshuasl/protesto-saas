"""
Utilitários RTF portados do fluxo Node (limparTagRTF / extrairVariaveis / limparArtefatosHtml).
Usados na normalização de tags, extração de variáveis e limpeza de HTML do LibreOffice.
"""

from __future__ import annotations

import re
from typing import TypedDict

# Marcadores de variável no RTF (\'AB = «, \'BB = »)
_RTF_VAR_SEGMENT = r"(?:[a-zA-Z0-9\s]|\\u\d+\s?\??|\\'[\dA-Fa-f]{2})+"
_REGEX_VARIAVEIS_MANUAIS = re.compile(rf"{_RTF_VAR_SEGMENT}\\'ABm\\'BB", re.IGNORECASE)
_REGEX_VARIAVEIS_AUTO = re.compile(rf"{_RTF_VAR_SEGMENT}\\'ABa\\'BB", re.IGNORECASE)

# Substituições de limparTagRTF (ordem importa para tokens mais longos)
_RTF_TAG_REPLACEMENTS: tuple[tuple[str, str], ...] = (
    (r"\\'AB", "«"),
    (r"\\'BB", "»"),
    (r"\\u8226\s?\??", "•"),
    (r"\\'E7", "ç"),
    (r"\\'E3", "ã"),
    (r"\\'BA", "º"),
    (r"\\'F5", "õ"),
    (r"\\'ED", "í"),
    (r"\\'E1", "á"),
    (r"\\'F3", "ó"),
    (r"\\'E9", "é"),
    (r"\\'FA", "ú"),
    (r"\\'C7", "Ç"),
)


class RtfVariaveisExtraidas(TypedDict):
    manuais: list[str]
    automaticas: list[str]


def limpar_tag_rtf(tag: str) -> str:
    """Converte trecho RTF em texto legível (equivalente a limparTagRTF)."""
    if not tag:
        return ""

    cleaned = tag
    for pattern, replacement in _RTF_TAG_REPLACEMENTS:
        cleaned = re.sub(pattern, replacement, cleaned, flags=re.IGNORECASE)

    return re.sub(r"[\r\n\t]+", " ", cleaned).strip()


def extrair_variaveis_do_rtf_content(conteudo_rtf: str) -> RtfVariaveisExtraidas:
    """Extrai variáveis manuais («m») e automáticas («a») do conteúdo RTF bruto."""
    if not conteudo_rtf:
        return RtfVariaveisExtraidas(manuais=[], automaticas=[])

    manuais_raw = _REGEX_VARIAVEIS_MANUAIS.findall(conteudo_rtf)
    auto_raw = _REGEX_VARIAVEIS_AUTO.findall(conteudo_rtf)

    manuais = list(dict.fromkeys(limpar_tag_rtf(item) for item in manuais_raw if item))
    automaticas = list(dict.fromkeys(limpar_tag_rtf(item) for item in auto_raw if item))

    return RtfVariaveisExtraidas(manuais=manuais, automaticas=automaticas)


def limpar_artefatos_html(html: str) -> str:
    """Remove âncoras vazias e artefatos do HTML gerado pelo LibreOffice."""
    if not html:
        return ""

    cleaned = html
    cleaned = re.sub(r'<a name=".*?"></a>', "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(
        r'<font face="Wingdings">.*?</font>',
        "ã",
        cleaned,
        flags=re.IGNORECASE | re.DOTALL,
    )
    cleaned = re.sub(r"[\r\n\t]+", " ", cleaned)
    cleaned = re.sub(r">\s+<", "><", cleaned)
    return cleaned.strip()
