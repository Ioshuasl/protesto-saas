import base64
import numbers
import re
import zlib
import zipfile
from io import BytesIO

from striprtf.striprtf import rtf_to_text


class Text:
    _RE_XML_TAGS = re.compile(r"<[^>]+>")
    _RE_SCRIPT = re.compile(r"<script.*?>.*?</script>", re.S | re.I)
    _RE_STYLE = re.compile(r"<style.*?>.*?</style>", re.S | re.I)
    _RE_HTML_TAGS = re.compile(r"<[^>]+>")

    @staticmethod
    def _is_empty(value) -> bool:
        if value is None:
            return True
        if isinstance(value, (str, bytes, bytearray, memoryview)):
            return len(value) == 0
        return False

    @staticmethod
    def normalize_binary(vf_string):
        if Text._is_empty(vf_string):
            return b""

        if hasattr(vf_string, "read"):
            try:
                vf_string = vf_string.read()
            except Exception:
                return b""

        if Text._is_empty(vf_string):
            return b""

        if isinstance(vf_string, bytes):
            raw_bytes = vf_string
        elif isinstance(vf_string, str):
            # Preserve 1:1 byte mapping when arbitrary bytes were materialized as str.
            raw_bytes = vf_string.encode("latin1", errors="ignore")
        elif isinstance(vf_string, numbers.Number):
            raw_bytes = str(vf_string).encode("utf-8", errors="ignore")
        else:
            try:
                raw_bytes = bytes(vf_string)
            except Exception:
                return b""

        if len(raw_bytes) > 16:
            try:
                decoded = base64.b64decode(raw_bytes, validate=True)
                if decoded and len(decoded) > 8:
                    raw_bytes = decoded
            except Exception:
                pass

        if raw_bytes.startswith(b"PK\x03\x04"):
            return raw_bytes

        if raw_bytes.lstrip().startswith(b"{\\rtf"):
            return raw_bytes

        if len(raw_bytes) > 2 and raw_bytes[0] == 0x78:
            try:
                decompressed = zlib.decompress(raw_bytes)
                if decompressed:
                    raw_bytes = decompressed
            except Exception:
                pass

        return raw_bytes

    @staticmethod
    def _decode_bytes(raw: bytes) -> str:
        for encoding in ("utf-8", "cp1252", "latin1"):
            try:
                return raw.decode(encoding)
            except UnicodeDecodeError:
                continue
            except Exception:
                break
        return raw.decode("latin1", errors="replace")

    @staticmethod
    def decompress_bytes(vf_string):
        return Text.normalize_binary(vf_string)

    @staticmethod
    def decompress(vf_string):
        raw = Text.normalize_binary(vf_string)
        if not raw:
            return ""
        return Text._decode_bytes(raw)

    @staticmethod
    def compress(text, *, encoding: str = "iso-8859-1"):
        if text is None:
            return b""

        if hasattr(text, "read"):
            raw = text.read()
        else:
            raw = text

        if isinstance(raw, str):
            raw = raw.encode(encoding, errors="ignore")
        else:
            raw = bytes(raw)

        return zlib.compress(raw)

    @staticmethod
    def plain(value) -> str:
        if value is None:
            return ""

        raw_bytes = Text.normalize_binary(value)
        if not raw_bytes:
            return ""

        if raw_bytes.startswith(b"PK\x03\x04"):
            try:
                with zipfile.ZipFile(BytesIO(raw_bytes)) as docx:
                    xml = docx.read("word/document.xml")
                    text = xml.decode("utf-8", errors="ignore")
                    text = text.replace("</w:p>", "\n")
                    text = Text._RE_XML_TAGS.sub("", text)
                    return text.strip()
            except Exception:
                return ""

        text = Text._decode_bytes(raw_bytes)
        if not text:
            return ""

        text = text.strip()

        if text.lstrip().startswith("{\\rtf"):
            try:
                return rtf_to_text(text).strip()
            except Exception:
                return text

        lower = text.lower()
        if "<html" in lower or "<body" in lower or "<p" in lower:
            try:
                text = Text._RE_SCRIPT.sub("", text)
                text = Text._RE_STYLE.sub("", text)
                text = Text._RE_HTML_TAGS.sub("", text)
                return text.strip()
            except Exception:
                return text

        return text.strip()
