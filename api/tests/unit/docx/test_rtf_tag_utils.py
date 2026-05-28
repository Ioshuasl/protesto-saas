import pytest

from actions.data.rtf_tag_utils import (
    extrair_variaveis_do_rtf_content,
    limpar_artefatos_html,
    limpar_tag_rtf,
)


@pytest.mark.unit
def test_limpar_tag_rtf_hex_and_guillemets():
    raw = r"CERTIDAO\'EDNOME\'ABm\'BB"
    cleaned = limpar_tag_rtf(raw)
    assert "í" in cleaned
    assert "«m»" in cleaned


@pytest.mark.unit
def test_extrair_variaveis_manuais_e_automaticas():
    rtf = (
        r"texto \'ABm\'BB "
        r"outro \'ABa\'BB "
        r"\'ABm\'BB"
    )
    vars_ = extrair_variaveis_do_rtf_content(rtf)
    assert any("m" in v for v in vars_["manuais"])
    assert any("a" in v for v in vars_["automaticas"])


@pytest.mark.unit
def test_limpar_artefatos_html():
    html = '<a name="anchor"></a><p>manifestação</p>'
    assert 'name="anchor"' not in limpar_artefatos_html(html)
