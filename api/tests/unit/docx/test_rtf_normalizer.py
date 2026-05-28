import pytest

from actions.data.rtf_normalizer import (
    deduplicate_rtf_unicode,
    is_wptools_legacy_rtf,
    normalize_rtf_for_storage,
    plain_text_to_simple_ansi_rtf,
    prepare_rtf_for_libreoffice,
    promote_rtf_ansi_to_unicode,
    should_promote_ansi_to_unicode,
)


@pytest.mark.unit
def test_should_promote_legacy_hex_rtf():
    rtf = r"{\rtf1\ansi\ansicpg1252 cart\'f3rio}"
    assert should_promote_ansi_to_unicode(rtf) is True


@pytest.mark.unit
def test_should_not_promote_unicode_rtf_from_libreoffice():
    rtf = r"{\rtf1\ansi\uc1\ansicpg1252 cart\u243?\'f3rio}"
    assert should_promote_ansi_to_unicode(rtf) is False


@pytest.mark.unit
def test_promote_hex_escape_without_duplicating_accent():
    rtf = r"{\rtf1\ansi\ansicpg1252 cart\'f3rio}"
    promoted = promote_rtf_ansi_to_unicode(rtf)
    assert promoted.count("\\u243?") == 1
    assert "óó" not in promoted


@pytest.mark.unit
def test_deduplicate_libreoffice_unicode_with_hex_fallback():
    """LibreOffice grava \\u237\\'ed (sem ?) para 'í'."""
    rtf = r"T\u237\'edtulo teste"
    cleaned = normalize_rtf_for_storage(rtf)
    assert cleaned == r"T\u237?tulo teste"
    assert "\\'ed" not in cleaned
    assert "íí" not in cleaned


@pytest.mark.unit
def test_deduplicate_unicode_escape_and_fallback_char():
    rtf = r"{\rtf1\ansi\uc1 cart\u243?ório}"
    cleaned = deduplicate_rtf_unicode(rtf)
    assert cleaned.count("\\u243?") == 1
    assert "óó" not in cleaned


@pytest.mark.unit
def test_deduplicate_repeated_guillemets_markers():
    rtf = r"nome \u171?\u171?\u171?\u171?CERTIDAO\u187?\u187?"
    cleaned = deduplicate_rtf_unicode(rtf)
    assert cleaned.count("\\u171?") == 1
    assert cleaned.count("\\u187?") == 1


@pytest.mark.unit
def test_ansi_escape_literal_guillemets_and_accents():
    rtf = r"{\rtf1\ansi at\'e9 «w»CERTIDAO cartório}"
    prepared, encoding = prepare_rtf_for_libreoffice(rtf)
    assert encoding == "cp1252"
    assert "«" not in prepared
    assert "\\'ab" in prepared.lower()
    assert "\\'bb" in prepared.lower()
    assert "\\'f3" in prepared.lower() or "\\'f3" in prepared


@pytest.mark.unit
def test_wptools_legacy_detection():
    rtf = r"{\rtf1\generator WPTools_5.202 \f1\wpprot1 «w»VAR«w»}"
    assert is_wptools_legacy_rtf(rtf) is True


@pytest.mark.unit
def test_plain_text_to_simple_ansi_rtf_preserves_guillemets():
    rtf = plain_text_to_simple_ansi_rtf("«w»CERTIDAO_TEMPO_PESQUISA«w»")
    assert "\\'ab" in rtf.lower()
    assert "\\'bb" in rtf.lower()
    assert "CERTIDAO_TEMPO_PESQUISA" in rtf


@pytest.mark.unit
def test_prepare_rtf_for_libreoffice_keeps_unicode_rtf():
    rtf = r"{\rtf1\ansi\uc1\ansicpg1252 certid\u227?o}"
    prepared, encoding = prepare_rtf_for_libreoffice(rtf)
    assert encoding == "cp1252"
    assert "\\u227?" in prepared or "\\'e3" in prepared.lower()
