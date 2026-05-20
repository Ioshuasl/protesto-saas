from __future__ import annotations

import os
import shutil
import subprocess
import uuid
from pathlib import Path
from typing import Literal, Optional

import fitz
from fastapi import HTTPException, status

from actions.data.base64 import Base64
from actions.data.text import Text


class DOCXConvertToPDFService:
    DOCX_MAGIC = b"PK\x03\x04"

    def execute(
        self,
        input_content,
        *,
        output: Literal["binary", "base64", "path"] = "base64",
        save_disk: bool = False,
        storage_dir: str = "./storage/temp",
        filename_prefix: Optional[str] = None,
        soffice_path: Optional[str] = None,
        convert_timeout_sec: int = 180,
    ) -> dict:
        docx_bytes = self._to_docx_bytes(input_content, storage_dir=storage_dir)
        pdf_bytes = self._convert_docx_bytes_to_pdf(
            docx_bytes=docx_bytes,
            storage_dir=storage_dir,
            filename_prefix=filename_prefix,
            soffice_path=soffice_path,
            convert_timeout_sec=convert_timeout_sec,
        )

        pages = self._count_pdf_pages(pdf_bytes)

        filename = None
        if output == "path" or save_disk:
            filename = self._save_pdf_to_disk(
                pdf_bytes=pdf_bytes,
                storage_dir=storage_dir,
                filename_prefix=filename_prefix,
            )

        if output == "path":
            pdf_value = filename or ""
        elif output == "binary":
            pdf_value = pdf_bytes
        else:
            pdf_value = Base64.encode(pdf_bytes)

        return {
            "pages": pages,
            "pdf": pdf_value,
            "filename": filename,
        }

    def _resolve_soffice_path(self, explicit_path: Optional[str] = None) -> str:
        if explicit_path:
            return explicit_path

        env_path = os.getenv("SOFFICE_PATH")
        if env_path:
            return env_path

        default_windows = r"C:\Program Files\LibreOffice\program\soffice.exe"
        if os.name == "nt":
            if Path(default_windows).exists():
                return default_windows
            return shutil.which("soffice") or default_windows

        return shutil.which("soffice") or shutil.which("libreoffice") or "soffice"

    def _to_docx_bytes(self, input_content, *, storage_dir: str) -> bytes:
        if isinstance(input_content, Path):
            return self._read_docx_file(input_content)

        if isinstance(input_content, str):
            path_value = self._try_resolve_path(input_content, storage_dir)
            if path_value is not None:
                return self._read_docx_file(path_value)

        decoded = Base64.decode(input_content)
        normalized = Text.normalize_binary(decoded)

        if not isinstance(normalized, (bytes, bytearray)):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Conteudo DOCX invalido.",
            )

        docx_bytes = bytes(normalized)
        if not docx_bytes.startswith(self.DOCX_MAGIC):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Conteudo informado nao e um DOCX valido.",
            )

        return docx_bytes

    def _try_resolve_path(self, raw: str, storage_dir: str) -> Optional[Path]:
        value = (raw or "").strip()
        if not value:
            return None

        direct = Path(value)
        if direct.exists() and direct.is_file():
            return direct

        relative = Path(storage_dir) / value
        if relative.exists() and relative.is_file():
            return relative

        return None

    def _read_docx_file(self, path: Path) -> bytes:
        try:
            data = path.resolve().read_bytes()
        except OSError:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Nao foi possivel ler o arquivo DOCX: {path}",
            )

        if not data.startswith(self.DOCX_MAGIC):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Arquivo informado nao e um DOCX valido.",
            )

        return data

    def _convert_docx_bytes_to_pdf(
        self,
        *,
        docx_bytes: bytes,
        storage_dir: str,
        filename_prefix: Optional[str],
        soffice_path: Optional[str],
        convert_timeout_sec: int,
    ) -> bytes:
        directory = Path(storage_dir).resolve()
        directory.mkdir(parents=True, exist_ok=True)

        base = self._build_base_name(filename_prefix=filename_prefix)
        docx_path = directory / f"{base}.docx"
        pdf_path = directory / f"{base}.pdf"

        docx_path.write_bytes(docx_bytes)

        cmd = [
            self._resolve_soffice_path(soffice_path),
            "--headless",
            "--nologo",
            "--nolockcheck",
            "--nodefault",
            "--nofirststartwizard",
            "--convert-to",
            "pdf",
            "--outdir",
            str(directory),
            str(docx_path),
        ]

        env = os.environ.copy()
        env.setdefault("LANG", "C.UTF-8")
        env.setdefault("LC_ALL", "C.UTF-8")

        try:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=int(convert_timeout_sec),
                env=env,
            )
        except subprocess.TimeoutExpired:
            self._cleanup_files(docx_path, pdf_path)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Timeout ao converter DOCX para PDF.",
            )
        except OSError as exc:
            self._cleanup_files(docx_path, pdf_path)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Falha ao executar LibreOffice: {exc}",
            )

        if result.returncode != 0:
            self._cleanup_files(docx_path, pdf_path)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.stderr
                or result.stdout
                or "Falha ao converter DOCX para PDF.",
            )

        if not pdf_path.exists():
            self._cleanup_files(docx_path, pdf_path)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="PDF nao foi gerado pela conversao.",
            )

        pdf_bytes = pdf_path.read_bytes()
        self._cleanup_files(docx_path, pdf_path)
        return pdf_bytes

    def _count_pdf_pages(self, pdf_bytes: bytes) -> int:
        if not pdf_bytes:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="PDF vazio apos conversao.",
            )

        try:
            with fitz.open(stream=pdf_bytes, filetype="pdf") as document:
                return int(document.page_count)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Nao foi possivel contar as paginas do PDF gerado.",
            )

    def _save_pdf_to_disk(
        self,
        *,
        pdf_bytes: bytes,
        storage_dir: str,
        filename_prefix: Optional[str],
    ) -> str:
        directory = Path(storage_dir).resolve()
        directory.mkdir(parents=True, exist_ok=True)

        base = self._build_base_name(filename_prefix=filename_prefix)
        filename = f"{base}.pdf"
        path = directory / filename
        path.write_bytes(pdf_bytes)
        return filename

    def _build_base_name(self, *, filename_prefix: Optional[str]) -> str:
        prefix = (filename_prefix or "docx_to_pdf").strip().replace(" ", "_")
        return f"{prefix}_{uuid.uuid4().hex}"

    def _cleanup_files(self, *paths: Path) -> None:
        for path in paths:
            try:
                if path.exists():
                    path.unlink()
            except Exception:
                pass
