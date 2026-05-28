from __future__ import annotations

import re

from striprtf.striprtf import rtf_to_text

_RTF_ANSICPG_RE = re.compile(r"\\ansicpg(\d+)", re.IGNORECASE)
_RTF_UC_RE = re.compile(r"\\uc\d+", re.IGNORECASE)
_RTF_HEX_ESCAPE_RE = re.compile(r"\\'[0-9a-fA-F]{2}")
_RTF_UNICODE_ESCAPE_RE = re.compile(r"\\u-?\d+\?")
_DUPLICATE_UNICODE_ESCAPE_RE = re.compile(r"(\\u-?\d+\?)(?:\1)+")
_UNICODE_HEX_FALLBACK_RE = re.compile(
    r"\\u(-?\d+)\??\\'([0-9a-fA-F]{2})",
    re.IGNORECASE,
)
_REDUNDANT_UNICODE_LITERAL_FALLBACK_RE = re.compile(
    r"\\u(-?\d+)\?([^\\{}\r\n])",
)

_CODEPAGE_ALIASES = {
    "1252": "cp1252",
    "1250": "cp1250",
    "1251": "cp1251",
    "1253": "cp1253",
    "1254": "cp1254",
    "28591": "latin1",
    "65001": "utf-8",
}


def detect_rtf_encoding_from_bytes(raw: bytes) -> str:
    head = raw[:512].decode("ascii", errors="ignore")
    match = _RTF_ANSICPG_RE.search(head)
    if not match:
        return "cp1252"
    return _CODEPAGE_ALIASES.get(match.group(1), f"cp{match.group(1)}")


def decode_rtf_bytes(raw: bytes) -> str:
    if not raw:
        return ""

    for encoding in (detect_rtf_encoding_from_bytes(raw), "utf-8", "cp1252", "latin1"):
        try:
            return raw.decode(encoding)
        except (UnicodeDecodeError, LookupError):
            continue
    return raw.decode("latin1", errors="replace")


def should_promote_ansi_to_unicode(rtf: str) -> bool:
    if not rtf or not rtf.lstrip().startswith("{\\rtf"):
        return False

    head = rtf[:512]
    if _RTF_UC_RE.search(head):
        return False
    if re.search(r"\\ansicpg65001", head, re.IGNORECASE):
        return False
    if _RTF_UNICODE_ESCAPE_RE.search(rtf) and not _RTF_HEX_ESCAPE_RE.search(rtf):
        return False

    return bool(_RTF_HEX_ESCAPE_RE.search(rtf))


def _rtf_unicode_codepoint(value: str) -> int:
    codepoint = int(value)
    if codepoint < 0:
        codepoint += 65536
    return codepoint


def _hex_escape_codepoint(hex_pair: str, encoding: str) -> int | None:
    try:
        return ord(bytes.fromhex(hex_pair).decode(encoding))
    except Exception:
        return None


def deduplicate_rtf_unicode(rtf: str, *, source_encoding: str | None = None) -> str:
    if not rtf:
        return rtf

    encoding = source_encoding or detect_rtf_encoding_from_bytes(
        rtf.encode("ascii", errors="ignore")
    )

    cleaned = _DUPLICATE_UNICODE_ESCAPE_RE.sub(r"\1", rtf)

    def _strip_hex_fallback(match: re.Match[str]) -> str:
        codepoint = _rtf_unicode_codepoint(match.group(1))
        hex_codepoint = _hex_escape_codepoint(match.group(2), encoding)
        if hex_codepoint is not None and hex_codepoint == codepoint:
            return f"\\u{match.group(1)}?"
        return match.group(0)

    cleaned = _UNICODE_HEX_FALLBACK_RE.sub(_strip_hex_fallback, cleaned)

    def _strip_literal_fallback(match: re.Match[str]) -> str:
        codepoint = _rtf_unicode_codepoint(match.group(1))
        fallback = match.group(2)
        if fallback and ord(fallback) == codepoint:
            return f"\\u{match.group(1)}?"
        return match.group(0)

    cleaned = _REDUNDANT_UNICODE_LITERAL_FALLBACK_RE.sub(
        _strip_literal_fallback, cleaned
    )
    return _DUPLICATE_UNICODE_ESCAPE_RE.sub(r"\1", cleaned)


def normalize_rtf_for_storage(rtf: str) -> str:
    """Normaliza RTF antes de gravar no BLOB ou abrir no LibreOffice."""
    return deduplicate_rtf_unicode(rtf)


def _char_to_rtf_hex_escape(ch: str, encoding: str) -> str:
    """Converte um caractere acentuado/símbolo para \\'XX (cp1252) ou \\uN?."""
    guillemets = {
        "\u00ab": r"\'ab",  # «
        "\u00bb": r"\'bb",  # »
    }
    if ch in guillemets:
        return guillemets[ch]

    try:
        data = ch.encode(encoding)
    except Exception:
        data = ch.encode("cp1252", errors="replace")

    if len(data) == 1:
        return f"\\'{data[0]:02x}"

    codepoint = ord(ch)
    if codepoint > 32767:
        codepoint -= 65536
    return f"\\u{codepoint}?"


def ansi_escape_literal_high_chars(rtf: str, *, encoding: str | None = None) -> str:
    """
    Converte caracteres Unicode literais no corpo do RTF para escapes ANSI \\'XX.
    Necessário para minutas legadas (WPTools) com «w» e acentos em texto puro.
    """
    if not rtf:
        return rtf

    source_encoding = encoding or detect_rtf_encoding_from_bytes(
        rtf.encode("ascii", errors="ignore")
    )

    resultado: list[str] = []
    i = 0
    while i < len(rtf):
        ch = rtf[i]

        if ch == "\\":
            if i + 3 < len(rtf) and rtf[i + 1] == "'":
                resultado.append(rtf[i : i + 4])
                i += 4
                continue

            start = i
            i += 1

            if i < len(rtf) and rtf[i] in "\\{}":
                resultado.append(rtf[start : i + 1])
                i += 1
                continue

            while i < len(rtf) and rtf[i].isalpha():
                i += 1

            if i < len(rtf) and rtf[i] in "+-":
                i += 1

            while i < len(rtf) and rtf[i].isdigit():
                i += 1

            if i < len(rtf) and rtf[i] == " ":
                i += 1

            resultado.append(rtf[start:i])
            continue

        if ch in "{}":
            resultado.append(ch)
            i += 1
            continue

        if ord(ch) >= 128:
            resultado.append(_char_to_rtf_hex_escape(ch, source_encoding))
            i += 1
            continue

        resultado.append(ch)
        i += 1

    return "".join(resultado)


def is_wptools_legacy_rtf(rtf: str) -> bool:
    """Detecta RTF gerado pelo WPTools (minutas legadas com wpprot / «w»)."""
    if not rtf:
        return False
    sample = rtf[:4000].lower()
    markers = (
        "wptools",
        "wpprot",
        "bkmkstart wel",
        "generator wptools",
    )
    return any(marker in sample for marker in markers)


def plain_text_to_simple_ansi_rtf(text: str, *, encoding: str = "cp1252") -> str:
    """Reconstrói RTF ANSI mínimo a partir de texto puro (compatível com LibreOffice)."""
    body_parts: list[str] = []
    for ch in text or "":
        if ch == "\n":
            body_parts.append(r"\par ")
        elif ch == "\r":
            continue
        elif ch in "\\{}":
            body_parts.append(f"\\{ch}")
        elif ord(ch) < 128:
            body_parts.append(ch)
        else:
            body_parts.append(_char_to_rtf_hex_escape(ch, encoding))

    body = "".join(body_parts)
    return (
        r"{\rtf1\ansi\ansicpg1252\deff0{\fonttbl{\f0\froman Times New Roman;}}"
        r"\f0\fs24 "
        + body
        + "}"
    )


def rebuild_wptools_rtf_for_libreoffice(rtf: str) -> str:
    """
    WPTools gera RTF que o LibreOffice não converte bem para DOCX.
    Extrai texto com striprtf e remonta um RTF ANSI simples.
    """
    plain = (rtf_to_text(rtf) or "").strip()
    if not plain:
        return r"{\rtf1\ansi\ansicpg1252\deff0{\fonttbl{\f0 Times New Roman;}}\f0\fs24 }"
    return plain_text_to_simple_ansi_rtf(plain)


def ensure_rtf_ansi_codepage(rtf: str, codepage: str = "1252") -> str:
    if not rtf or not rtf.lstrip().startswith("{\\rtf"):
        return rtf

    head = rtf[:512]
    if _RTF_ANSICPG_RE.search(head):
        return rtf

    marker = "{\\rtf1\\ansi"
    if marker in rtf[:32]:
        return rtf.replace(marker, f"{marker}\\ansicpg{codepage}", 1)
    return rtf


def promote_rtf_ansi_to_unicode(rtf: str) -> str:
    if not should_promote_ansi_to_unicode(rtf):
        return rtf

    if rtf.startswith("{\\rtf1\\ansi") and "\\uc" not in rtf[:32]:
        rtf = rtf.replace("{\\rtf1\\ansi", "{\\rtf1\\ansi\\uc1", 1)

    source_encoding = detect_rtf_encoding_from_bytes(
        rtf.encode("ascii", errors="ignore")
    )

    resultado: list[str] = []
    i = 0
    while i < len(rtf):
        ch = rtf[i]

        if ch == "\\":
            if i + 3 < len(rtf) and rtf[i + 1] == "'":
                hex_pair = rtf[i + 2 : i + 4]
                try:
                    decoded = bytes.fromhex(hex_pair).decode(source_encoding)
                    resultado.append(_rtf_unicode_escape(decoded))
                    i += 4
                    continue
                except Exception:
                    pass

            start = i
            i += 1

            if i < len(rtf) and rtf[i] in "\\{}":
                resultado.append(rtf[start : i + 1])
                i += 1
                continue

            while i < len(rtf) and rtf[i].isalpha():
                i += 1

            if i < len(rtf) and rtf[i] in "+-":
                i += 1

            while i < len(rtf) and rtf[i].isdigit():
                i += 1

            if i < len(rtf) and rtf[i] == " ":
                i += 1

            resultado.append(rtf[start:i])
            continue

        if ch in "{}":
            resultado.append(ch)
            i += 1
            continue

        if ord(ch) < 128:
            resultado.append(ch)
        else:
            resultado.append(_rtf_unicode_escape(ch))
        i += 1

    return deduplicate_rtf_unicode("".join(resultado))


def prepare_rtf_for_libreoffice(rtf: str) -> tuple[str, str]:
    """
    Prepara RTF legado ou gerado pelo LibreOffice para conversão headless.

    - WPTools: striprtf + RTF ANSI simples (preserva «w» e acentos no DOCX).
    - Demais: deduplica Unicode e converte literais para \\'XX (cp1252).
    """
    cleaned = normalize_rtf_for_storage(rtf)

    if is_wptools_legacy_rtf(cleaned):
        return rebuild_wptools_rtf_for_libreoffice(cleaned), "cp1252"

    cleaned = ansi_escape_literal_high_chars(cleaned)
    cleaned = ensure_rtf_ansi_codepage(cleaned)
    return cleaned, "cp1252"


def _rtf_unicode_escape(text: str) -> str:
    escaped: list[str] = []
    for ch in text:
        codepoint = ord(ch)
        if codepoint > 32767:
            codepoint -= 65536
        escaped.append(f"\\u{codepoint}?")
    return "".join(escaped)
