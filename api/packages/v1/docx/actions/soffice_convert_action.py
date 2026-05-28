from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from fastapi import HTTPException, status

from actions.env.env_config_loader import EnvConfigLoader


class SofficeConvertAction:
    """Conversão headless via LibreOffice (soffice), equivalente ao fluxo Node."""

    _FORMAT_EXT = {
        "rtf": ".rtf",
        "docx": ".docx",
        "html": ".html",
        "pdf": ".pdf",
    }

    @staticmethod
    def resolve_soffice_path() -> str:
        env = EnvConfigLoader(env_file=".env")
        configured = getattr(env, "SOFFICE_PATH", None)
        if configured:
            return str(configured)

        if os.name != "nt":
            return shutil.which("soffice") or shutil.which("libreoffice") or "soffice"

        default_windows = r"C:\Program Files\LibreOffice\program\soffice.exe"
        if Path(default_windows).exists():
            return default_windows
        return shutil.which("soffice") or default_windows

    @classmethod
    def convert_file(
        cls,
        input_path: Path,
        output_format: str,
        outdir: Path | None = None,
        *,
        timeout_sec: int = 120,
    ) -> Path:
        output_format = output_format.lower().strip(".")
        if output_format not in cls._FORMAT_EXT:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Formato de saída não suportado: {output_format}",
            )

        input_path = input_path.resolve()
        if not input_path.exists():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Arquivo de entrada não encontrado: {input_path}",
            )

        target_dir = (outdir or input_path.parent).resolve()
        target_dir.mkdir(parents=True, exist_ok=True)

        cmd = [
            cls.resolve_soffice_path(),
            "--headless",
            "--nologo",
            "--nolockcheck",
            "--nodefault",
            "--nofirststartwizard",
            "--convert-to",
            output_format,
            "--outdir",
            str(target_dir),
            str(input_path),
        ]

        env = os.environ.copy()
        env.setdefault("LANG", "C.UTF-8")
        env.setdefault("LC_ALL", "C.UTF-8")

        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=int(timeout_sec),
            env=env,
        )

        if result.returncode != 0:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.stderr
                or result.stdout
                or f"Falha ao converter {input_path.name} para {output_format}.",
            )

        output_path = target_dir / f"{input_path.stem}{cls._FORMAT_EXT[output_format]}"
        if not output_path.exists():
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=(
                    f"Conversão para {output_format} não gerou arquivo de saída "
                    f"({output_path.name})."
                ),
            )

        return output_path

    @classmethod
    def convert_bytes(
        cls,
        file_bytes: bytes,
        input_format: str,
        output_format: str,
        *,
        input_basename: str = "input",
        timeout_sec: int = 120,
    ) -> bytes:
        input_format = input_format.lower().strip(".")
        output_format = output_format.lower().strip(".")

        with tempfile.TemporaryDirectory(prefix="soffice_convert_") as temp_dir:
            temp_path = Path(temp_dir)
            input_file = temp_path / f"{input_basename}.{input_format}"
            input_file.write_bytes(file_bytes)

            output_file = cls.convert_file(
                input_file,
                output_format,
                temp_path,
                timeout_sec=timeout_sec,
            )
            return output_file.read_bytes()
