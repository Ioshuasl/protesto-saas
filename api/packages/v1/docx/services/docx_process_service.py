from __future__ import annotations

import base64
import os
import re
import shutil
import subprocess
import traceback
import uuid
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path
from typing import Any, Literal, Optional, Union

import requests
from docx import Document
from fastapi import HTTPException, status
from pydantic import BaseModel, Field
from striprtf.striprtf import rtf_to_text

from actions.data.rtf_normalizer import (
    deduplicate_rtf_unicode,
    promote_rtf_ansi_to_unicode,
    should_promote_ansi_to_unicode,
)
from actions.data.text import Text
from packages.v1.docx.services.docx_rtf_convert_service import DocxRtfConvertService


# ======================================================
# SOFFICE PATH (Windows/Linux/Docker)
# ======================================================
SOFFICE_PATH = r"C:\Program Files\LibreOffice\program\soffice.exe"

if os.getenv("SOFFICE_PATH"):
    SOFFICE_PATH = os.getenv("SOFFICE_PATH") or SOFFICE_PATH
else:
    if os.name != "nt":
        SOFFICE_PATH = (
            shutil.which("soffice") or shutil.which("libreoffice") or "soffice"
        )
    else:
        try:
            if not Path(SOFFICE_PATH).exists():
                SOFFICE_PATH = shutil.which("soffice") or SOFFICE_PATH
        except OSError:
            SOFFICE_PATH = shutil.which("soffice") or SOFFICE_PATH


# ======================================================
# SCHEMA ÚNICO (ENTRADA)
# ======================================================
class DOCXProcessSchema(BaseModel):
    """
    Schema único para entrada.

    Entradas possíveis:
    - content: bytes | str | None
      Pode ser: DOCX binário, RTF string, texto comum, base64 (docx/rtf/texto), ou conteúdo comprimido.
    - source_url / onlyoffice_status:
      Se vierem, baixa o arquivo do OnlyOffice quando status in (2,6).

    Saídas controladas por output:
    - "path"    -> retorna o NOME do docx salvo (não retorna caminho absoluto)
    - "binary"  -> retorna bytes do docx
    - "base64"  -> retorna base64 do docx
    - "txt"     -> retorna texto puro (sem formatação), seja docx ou rtf ou texto
    """

    id: str = Field(..., description="Identificador para naming e rastreio")
    content: Optional[Union[bytes, str]] = Field(
        default=None, description="Conteúdo (docx/rtf/texto/base64/comprimido)"
    )

    # IO / Storage
    save_disk: bool = Field(default=False, description="Se True, salva DOCX em disco")
    storage_dir: str = Field(default="./storage/temp", description="Diretório de saída")
    filename_prefix: Optional[str] = Field(default=None, description="Prefixo opcional")
    output: Literal["path", "binary", "base64", "txt"] = Field(
        default="path", description="Tipo de retorno"
    )

    # OnlyOffice callback (opcional)
    source_url: Optional[str] = Field(default=None, description="URL do arquivo salvo")
    onlyoffice_status: Optional[int] = Field(
        default=None, description="Status do callback OnlyOffice (2/6 salva)"
    )
    download_timeout_sec: int = Field(default=30, description="Timeout do download")

    # Conversão
    soffice_path: str = Field(
        default=SOFFICE_PATH, description="Caminho do LibreOffice"
    )
    convert_timeout_sec: int = Field(default=180, description="Timeout do soffice")

    # Segurança/Robustez
    max_layers: int = Field(
        default=6, description="Máximo de camadas (base64/compress)"
    )
    invalid_text: str = Field(
        default="texto inválido",
        description="Texto a escrever quando não for possível acessar/decodificar",
    )


# ======================================================
# RESULTADO (RETORNO PADRÃO)
# ======================================================
@dataclass
class DOCXProcessResult:
    ok: bool
    output_type: Literal["path", "binary", "base64", "txt"]
    value: Union[str, bytes]
    path: Optional[str] = None
    warning: Optional[str] = None


# ======================================================
# CLASSE NOVA: DOCXProcess
# ======================================================
class DOCXProcess:
    """
    Classe única para:
    - Receber docx/rtf/texto (bytes/str), base64, comprimido (em múltiplas camadas)
    - Baixar do OnlyOffice (quando aplicável)
    - Converter RTF->DOCX
    - Criar DOCX em branco quando content vazio
    - Produzir saída como: docx salvo (nome), binário, base64, ou texto puro (txt)
    - Quando não conseguir acessar/decodificar, gera DOCX com "texto inválido" (ou txt puro)

    execute(...) retorna diretamente o valor final (str/bytes).
    """

    DOCX_MAGIC_BYTES = b"PK\x03\x04"
    DOCX_MAGIC_STR = "PK\x03\x04"
    _RTF_ANSICPG_RE = re.compile(r"\\ansicpg(\d+)")

    _B64_ALLOWED = set(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
    )

    # ======================================================
    # API PÚBLICA
    # ======================================================
    def execute(self, data: DOCXProcessSchema) -> Union[str, bytes]:
        try:
            if self._should_download(data):
                raw = self._download_bytes(data)
                return self._produce_from_any(data, raw, warning=None).value

            return self._produce_from_any(data, data.content, warning=None).value

        except HTTPException as e:
            return self._produce_invalid(
                data, warning=e.detail if hasattr(e, "detail") else str(e)
            ).value

        except Exception:
            print(traceback.format_exc(), flush=True)
            return self._produce_invalid(
                data, warning="Erro inesperado no processamento"
            ).value

    # ======================================================
    # CORE
    # ======================================================
    def _produce_from_any(
        self,
        data: DOCXProcessSchema,
        incoming: Optional[Union[bytes, str]],
        warning: Optional[str],
    ) -> DOCXProcessResult:

        if incoming is None or (
            isinstance(incoming, (bytes, str)) and len(incoming) == 0
        ):
            docx_bytes = self._create_blank_docx()
            return self._finalize(
                data, docx_bytes=docx_bytes, plain_text=None, warning=warning
            )

        resolved = self._unwrap_layers(data, incoming)

        if data.output == "txt":
            if resolved.docx_bytes is not None:
                txt = self._docx_bytes_to_plain_text(
                    resolved.docx_bytes, invalid_text=data.invalid_text
                )
                return DOCXProcessResult(
                    ok=True, output_type="txt", value=txt, warning=warning
                )

            if resolved.rtf_str is not None:
                txt = self._rtf_to_plain_text(
                    resolved.rtf_str, invalid_text=data.invalid_text
                )
                return DOCXProcessResult(
                    ok=True, output_type="txt", value=txt, warning=warning
                )

            if resolved.plain_text is not None:
                return DOCXProcessResult(
                    ok=True,
                    output_type="txt",
                    value=resolved.plain_text,
                    warning=warning,
                )

            return DOCXProcessResult(
                ok=False,
                output_type="txt",
                value=data.invalid_text,
                warning=warning or "Conteúdo inválido",
            )

        if resolved.docx_bytes is not None:
            return self._finalize(
                data,
                docx_bytes=resolved.docx_bytes,
                plain_text=resolved.plain_text,
                warning=warning,
            )

        if resolved.rtf_str is not None:
            docx_bytes = self._convert_rtf_str_to_docx_bytes(data, resolved.rtf_str)
            return self._finalize(
                data, docx_bytes=docx_bytes, plain_text=None, warning=warning
            )

        if resolved.plain_text is not None:
            docx_bytes = self._create_docx_with_text(resolved.plain_text)
            return self._finalize(
                data,
                docx_bytes=docx_bytes,
                plain_text=resolved.plain_text,
                warning=warning,
            )

        return self._produce_invalid(
            data, warning=warning or "Não foi possível resolver o conteúdo"
        )

    def _finalize(
        self,
        data: DOCXProcessSchema,
        docx_bytes: bytes,
        plain_text: Optional[str],
        warning: Optional[str],
    ) -> DOCXProcessResult:

        if not docx_bytes or not docx_bytes.startswith(self.DOCX_MAGIC_BYTES):
            docx_bytes = self._create_docx_with_text(data.invalid_text)

        filename: Optional[str] = None
        must_save = (data.output == "path") or bool(data.save_disk)

        if must_save:
            filename = self._save_docx_to_disk(data, docx_bytes)

        if data.output == "path":
            return DOCXProcessResult(
                ok=True,
                output_type="path",
                value=filename or "",
                path=filename,
                warning=warning,
            )

        if data.output == "binary":
            return DOCXProcessResult(
                ok=True,
                output_type="binary",
                value=docx_bytes,
                path=filename,
                warning=warning,
            )

        if data.output == "base64":
            b64 = base64.b64encode(docx_bytes).decode("ascii")
            return DOCXProcessResult(
                ok=True, output_type="base64", value=b64, path=filename, warning=warning
            )

        return DOCXProcessResult(
            ok=False,
            output_type=data.output,
            value=data.invalid_text,
            path=filename,
            warning=warning,
        )

    def _produce_invalid(
        self, data: DOCXProcessSchema, warning: Optional[str]
    ) -> DOCXProcessResult:
        if data.output == "txt":
            return DOCXProcessResult(
                ok=False, output_type="txt", value=data.invalid_text, warning=warning
            )

        docx_bytes = self._create_docx_with_text(data.invalid_text)
        return self._finalize(
            data, docx_bytes=docx_bytes, plain_text=data.invalid_text, warning=warning
        )

    # ======================================================
    # ONLYOFFICE
    # ======================================================
    def _should_download(self, data: DOCXProcessSchema) -> bool:
        if not data.source_url:
            return False
        if data.onlyoffice_status is None:
            return False
        return data.onlyoffice_status in (2, 6)

    def _download_bytes(self, data: DOCXProcessSchema) -> bytes:
        try:
            r = requests.get(data.source_url, timeout=data.download_timeout_sec)
            if r.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail="Falha ao baixar o arquivo do OnlyOffice.",
                )
            return r.content
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Falha inesperada ao baixar o arquivo do OnlyOffice.",
            )

    # ======================================================
    # UNWRAP (BASE64 / COMPRESS / DETECÇÃO)
    # ======================================================
    @dataclass
    class _Resolved:
        docx_bytes: Optional[bytes] = None
        rtf_str: Optional[str] = None
        plain_text: Optional[str] = None

    def _unwrap_layers(
        self, data: DOCXProcessSchema, incoming: Union[bytes, str]
    ) -> _Resolved:
        value: Any = incoming

        for _ in range(max(1, int(data.max_layers))):
            if isinstance(value, (bytes, bytearray)):
                b = bytes(value)

                if b.startswith(self.DOCX_MAGIC_BYTES):
                    return self._Resolved(docx_bytes=b)

                if b.lstrip().startswith(b"{\\rtf"):
                    return self._Resolved(rtf_str=self._decode_rtf_bytes(b))

                out = self._try_decompress_bytes(b)
                if out is not None and out != b:
                    value = out
                    continue

                if self._looks_like_base64_bytes(b):
                    s = b.decode("ascii", errors="ignore").strip()
                    decoded = self._b64decode_strict_or_none(s)
                    if decoded:
                        value = decoded
                        continue

                txt = self._bytes_to_text(b)
                if txt is not None:
                    t = txt.lstrip()
                    if t.startswith("{\\rtf"):
                        return self._Resolved(rtf_str=t)
                    if t.startswith(self.DOCX_MAGIC_STR):
                        return self._Resolved(
                            docx_bytes=t.encode("latin1", errors="ignore")
                        )
                    return self._Resolved(plain_text=txt)

                break

            if isinstance(value, str):
                s = value.strip()

                if s.startswith(self.DOCX_MAGIC_STR):
                    return self._Resolved(
                        docx_bytes=s.encode("latin1", errors="ignore")
                    )

                if s.lstrip().startswith("{\\rtf"):
                    return self._Resolved(rtf_str=s.lstrip())

                payload = self._strip_data_uri(s).strip()
                decoded = None
                if self._looks_like_base64_str(payload):
                    decoded = self._b64decode_strict_or_none(payload)
                if decoded:
                    value = decoded
                    continue

                b = payload.encode("utf-8", errors="ignore")
                out = self._try_decompress_bytes(b)
                if out is not None and out != b:
                    value = out
                    continue

                return self._Resolved(plain_text=s)

            break

        return self._Resolved()

    def _strip_data_uri(self, s: str) -> str:
        if "base64," in s:
            return s.split("base64,", 1)[1]
        return s

    def _looks_like_base64_str(self, s: str) -> bool:
        if not s:
            return False
        compact = "".join(s.split())
        if len(compact) < 16:
            return False
        return all(ch in self._B64_ALLOWED for ch in compact)

    def _looks_like_base64_bytes(self, b: bytes) -> bool:
        if not b or len(b) < 16:
            return False
        if any(x > 127 for x in b):
            return False
        s = b.decode("ascii", errors="ignore")
        return self._looks_like_base64_str(s)

    def _b64decode_strict_or_none(self, s: str) -> Optional[bytes]:
        compact = "".join(s.split())
        if not compact:
            return None

        missing = len(compact) % 4
        if missing:
            compact += "=" * (4 - missing)

        try:
            return base64.b64decode(compact, validate=True)
        except Exception:
            return None

    def _try_decompress_bytes(self, b: bytes) -> bytes | str | None:
        try:
            out = Text.decompress_bytes(b)
        except Exception:
            return None

        if out is None:
            return None
        if isinstance(out, (bytes, str)):
            return out
        return None

    def _bytes_to_text(self, b: bytes) -> Optional[str]:
        if not b:
            return ""
        for encoding in ("utf-8", "cp1252", "latin1"):
            try:
                return b.decode(encoding)
            except UnicodeDecodeError:
                continue
            except Exception:
                return None
        return b.decode("latin1", errors="replace")

    def _decode_rtf_bytes(self, b: bytes) -> str:
        codepage = self._detect_rtf_encoding(b) or "cp1252"

        for encoding in (codepage, "cp1252", "latin1"):
            try:
                return b.decode(encoding)
            except UnicodeDecodeError:
                continue
            except LookupError:
                continue
            except Exception:
                break

        return b.decode("latin1", errors="replace")

    def _detect_rtf_encoding(self, b: bytes) -> Optional[str]:
        head = b[:512].decode("ascii", errors="ignore")
        match = self._RTF_ANSICPG_RE.search(head)
        if not match:
            return None

        codepage = match.group(1)
        aliases = {
            "1252": "cp1252",
            "1250": "cp1250",
            "1251": "cp1251",
            "1253": "cp1253",
            "1254": "cp1254",
            "28591": "latin1",
            "65001": "utf-8",
        }
        return aliases.get(codepage, f"cp{codepage}")

    # ======================================================
    # RTF -> DOCX
    # ======================================================
    def _convert_rtf_str_to_docx_bytes(
        self, data: DOCXProcessSchema, rtf: str
    ) -> bytes:
        base = self._build_base_name(data)
        try:
            docx_bytes = DocxRtfConvertService.rtf_text_to_docx_bytes(
                rtf,
                storage_dir=data.storage_dir,
                base_name=base,
                timeout_sec=data.convert_timeout_sec,
            )
        except HTTPException:
            raise
        except Exception:
            return self._create_docx_with_text(data.invalid_text)

        if not docx_bytes.startswith(self.DOCX_MAGIC_BYTES):
            return self._create_docx_with_text(data.invalid_text)

        return docx_bytes

    # ======================================================
    # TXT EXTRACTION (RTF/DOCX)
    # ======================================================
    def _rtf_to_plain_text(self, rtf: str, invalid_text: str) -> str:
        try:
            normalized = deduplicate_rtf_unicode(rtf)
            if should_promote_ansi_to_unicode(normalized):
                normalized = promote_rtf_ansi_to_unicode(normalized)
            return (rtf_to_text(normalized) or "").strip()
        except Exception:
            return invalid_text

    def _docx_bytes_to_plain_text(self, docx_bytes: bytes, invalid_text: str) -> str:
        if not docx_bytes or not docx_bytes.startswith(self.DOCX_MAGIC_BYTES):
            return invalid_text

        try:
            bio = BytesIO(docx_bytes)
            doc = Document(bio)

            parts: list[str] = []

            for p in doc.paragraphs:
                t = (p.text or "").strip()
                if t:
                    parts.append(t)

            for table in doc.tables:
                for row in table.rows:
                    row_text: list[str] = []
                    for cell in row.cells:
                        cell_text = (cell.text or "").strip()
                        if cell_text:
                            row_text.append(cell_text)
                    if row_text:
                        parts.append(" | ".join(row_text))

            return "\n".join(parts).strip()

        except Exception:
            return invalid_text

    # ======================================================
    # DOCX CREATION
    # ======================================================
    def _create_blank_docx(self) -> bytes:
        buffer = BytesIO()
        doc = Document()
        doc.save(buffer)
        buffer.seek(0)
        return buffer.read()

    def _create_docx_with_text(self, text: str) -> bytes:
        buffer = BytesIO()
        doc = Document()
        doc.add_paragraph(text or "")
        doc.save(buffer)
        buffer.seek(0)
        return buffer.read()

    # ======================================================
    # RTF NORMALIZATION (UNICODE REAL)
    # ======================================================
    # ======================================================
    # DISK IO
    # ======================================================
    def _prepare_directory(self, storage_dir: str) -> Path:
        diretorio = Path(storage_dir).resolve()
        diretorio.mkdir(parents=True, exist_ok=True)
        return diretorio

    def _build_base_name(self, data: DOCXProcessSchema) -> str:
        prefix = (data.filename_prefix or "").strip()
        if prefix:
            prefix = prefix.replace(" ", "_")
            return f"{prefix}_{data.id}_{uuid.uuid4().hex}"
        return f"{data.id}_{uuid.uuid4().hex}"

    def _save_docx_to_disk(self, data: DOCXProcessSchema, docx_bytes: bytes) -> str:
        diretorio = self._prepare_directory(data.storage_dir)
        base = self._build_base_name(data)
        filename = f"{base}.docx"
        path = diretorio / filename
        path.write_bytes(docx_bytes)
        return filename  # <- retorna APENAS o nome do arquivo

    def _cleanup_files(self, *paths: Path) -> None:
        for p in paths:
            try:
                if p.exists():
                    p.unlink()
            except Exception:
                pass
