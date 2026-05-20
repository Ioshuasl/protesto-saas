import base64
import logging
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Optional, Literal

from PIL import Image, ImageSequence, UnidentifiedImageError

from actions.env.env_config_loader import EnvConfigLoader
from packages.v1.ged.actions.ged_base import GedBase
from packages.v1.ged.actions.ged_locator import GedLocator


ReturnType = Literal["path", "filename", "base64", "object"]
OutputFormat = Literal["jpg", "png", "pdf"]
PagePosition = Literal["first", "last"]


class GEDConvert(GedBase):
    _TIFF_SIGNATURES = (
        b"II*\x00",
        b"MM\x00*",
        b"II+\x00",
        b"MM\x00+",
    )

    def __init__(self, base_dir: Optional[str | Path | None] = None):
        env = EnvConfigLoader(env_file=".env")

        default_base = getattr(env, "GED_BASE_DIR", None) or getattr(env, "ORIUS_GED", None)
        super().__init__(base_dir or default_base)

    _INVALID_FILENAME_CHARS = re.compile(r'[<>:"/\\|?*#\x00-\x1f]')
    _logger = logging.getLogger(__name__)

    @classmethod
    def _is_tiff_header(cls, header: bytes) -> bool:
        return any(header.startswith(signature) for signature in cls._TIFF_SIGNATURES)

    @classmethod
    def _sanitize_filename(cls, name: str) -> str:
        if not name or not name.strip():
            return "arquivo"
        sanitized = cls._INVALID_FILENAME_CHARS.sub("_", name)
        sanitized = re.sub(r"_+", "_", sanitized)
        sanitized = sanitized.strip(" ._")
        return sanitized if sanitized else "arquivo"

    def convert(
        self,
        serventia: int,
        record_id: int | str,
        pasta: Optional[str] = None,
        filename_contains: Optional[str] = None,
        quality: int = 50,
        output_dir: str | Path | None = None,
        temp_dir: str | Path | None = None,
        return_type: ReturnType = "path",
        page_position: PagePosition = "first",
        output_format: OutputFormat = "jpg",
    ):
        debug_enabled = str(os.getenv("GED_CONVERT_DEBUG", "0")).strip().lower() in {
            "1",
            "true",
            "yes",
            "on",
        }
        debug_step = 0

        def debug_print(message: str, **context):
            nonlocal debug_step
            if not debug_enabled:
                return
            debug_step += 1
            ordered_context = " | ".join(f"{k}={v}" for k, v in context.items())
            if ordered_context:
                print(f"[GEDConvert][{debug_step:02d}] {message} | {ordered_context}")
                return
            print(f"[GEDConvert][{debug_step:02d}] {message}")

        record_id = int(record_id)
        debug_print(
            "inicio da conversao",
            serventia=serventia,
            record_id=record_id,
            pasta=pasta,
            base_dir=self.base_dir,
            cwd=os.getcwd(),
            output_format=output_format,
            return_type=return_type,
            output_dir=output_dir,
            temp_dir=temp_dir,
            page_position=page_position,
        )

        locator = GedLocator(self.base_dir)
        source = locator.locate(
            serventia=serventia,
            record_id=record_id,
            pasta=pasta,
            filename_contains=filename_contains or "",
            extensions=["tif", "tiff", "spd", "jpg", "jpeg", "png"],
            include_deleted=False,
        )
        debug_print("resultado do locator", source=source)

        if not source:
            debug_print("arquivo nao localizado no GED")
            return None

        source = Path(source).resolve()
        debug_print(
            "arquivo de origem resolvido",
            source_path=source,
            source_realpath=os.path.realpath(source),
            suffix=source.suffix.lower(),
            source_exists=source.exists(),
            source_is_file=source.is_file(),
            source_readable=os.access(source, os.R_OK),
            source_size=source.stat().st_size if source.exists() else "n/a",
        )
        if source.parent.exists():
            siblings = sorted([p.name for p in source.parent.iterdir() if p.is_file()])[:30]
            debug_print(
                "arquivos no diretorio de origem (max 30)",
                source_parent=source.parent,
                siblings_count=len(siblings),
                siblings=siblings,
            )
        else:
            debug_print("diretorio de origem nao existe", source_parent=source.parent)

        if output_dir:
            output_base = Path(output_dir).resolve()
        elif temp_dir:
            output_base = Path(temp_dir).resolve()
        else:
            raise ValueError("Informe output_dir ou temp_dir")

        output_base.mkdir(parents=True, exist_ok=True)
        debug_print("output_base preparado", output_base=output_base, exists=output_base.exists())

        if temp_dir:
            temp_base = Path(temp_dir).resolve()
            temp_base.mkdir(parents=True, exist_ok=True)
        else:
            temp_base = output_base
        debug_print("temp_base preparado", temp_base=temp_base, exists=temp_base.exists())

        spd_tiff_path: Path | None = None
        open_path = source
        header = source.read_bytes()[:16]
        debug_print("header lido", header_hex=header.hex(), header_len=len(header))

        if source.suffix.lower() == ".spd" and self._is_tiff_header(header):
            stem_safe = self._sanitize_filename(source.stem)
            spd_tiff_path = (temp_base / f".{stem_safe}.source.tif").resolve()
            spd_tiff_path.write_bytes(source.read_bytes())
            open_path = spd_tiff_path
            debug_print(
                "spd com assinatura tiff detectado",
                spd_tiff_path=spd_tiff_path,
                open_path=open_path,
            )
        else:
            debug_print(
                "spd sem assinatura tiff ou arquivo nao-spd",
                is_spd=(source.suffix.lower() == ".spd"),
                is_tiff_header=self._is_tiff_header(header),
                open_path=open_path,
            )

        try:
            debug_print(
                "abrindo imagem com pillow",
                open_path=open_path,
                open_path_realpath=os.path.realpath(open_path),
                open_exists=Path(open_path).exists(),
                open_is_file=Path(open_path).is_file(),
                open_readable=os.access(open_path, os.R_OK),
                open_size=Path(open_path).stat().st_size if Path(open_path).exists() else "n/a",
            )
            with Image.open(open_path) as img:
                debug_print(
                    "imagem aberta",
                    image_format=img.format,
                    image_mode=img.mode,
                    image_size=img.size,
                    n_frames=getattr(img, "n_frames", 1),
                )
                frames = [frame.copy().convert("RGB") for frame in ImageSequence.Iterator(img)]
                debug_print("frames convertidos para RGB", frames_count=len(frames))

                base_name = self._sanitize_filename(source.stem)
                if output_format == "jpg":
                    filename = f"{base_name}.jpg"
                elif output_format == "png":
                    filename = f"{base_name}.png"
                elif output_format == "pdf":
                    filename = f"{base_name}.pdf"
                else:
                    raise ValueError(f"Formato de saida invalido: {output_format}")

                final_path = (output_base / filename).resolve()
                tmp = (temp_base / f".{filename}.tmp").resolve()
                debug_print("destinos definidos", filename=filename, tmp=tmp, final_path=final_path)

                if output_format == "jpg":
                    if page_position not in {"first", "last"}:
                        raise ValueError("page_position invalido. Use 'first' ou 'last'.")
                    rgb = frames[0] if page_position == "first" else frames[-1]
                    rgb.save(tmp, format="JPEG", quality=quality, optimize=True)
                    debug_print("arquivo JPG temporario salvo", quality=quality, tmp_size=tmp.stat().st_size)
                elif output_format == "png":
                    if page_position not in {"first", "last"}:
                        raise ValueError("page_position invalido. Use 'first' ou 'last'.")
                    rgb = frames[0] if page_position == "first" else frames[-1]
                    rgb.save(tmp, format="PNG", optimize=True)
                    debug_print("arquivo PNG temporario salvo", tmp_size=tmp.stat().st_size)
                elif output_format == "pdf":
                    frames[0].save(
                        tmp,
                        format="PDF",
                        save_all=True,
                        append_images=frames[1:],
                    )
                    debug_print("arquivo PDF temporario salvo", tmp_size=tmp.stat().st_size)

                tmp.replace(final_path)
                debug_print(
                    "arquivo final movido",
                    final_path=final_path,
                    final_exists=final_path.exists(),
                    final_size=final_path.stat().st_size if final_path.exists() else "n/a",
                )
        except (UnidentifiedImageError, OSError, ValueError) as exc:
            debug_print("erro na conversao", error_type=type(exc).__name__, error=str(exc))
            self._logger.warning(
                "GEDConvert: arquivo de origem invalido para conversao",
                extra={
                    "source_path": str(source),
                    "open_path": str(open_path),
                    "output_format": output_format,
                },
            )
            return None
        finally:
            if spd_tiff_path and spd_tiff_path.exists():
                spd_tiff_path.unlink()
                debug_print("arquivo temporario spd_tiff removido", spd_tiff_path=spd_tiff_path)

        filename_on_disk = final_path.name
        debug_print("retorno preparado", filename_on_disk=filename_on_disk, return_type=return_type)

        if return_type == "filename":
            return filename_on_disk

        if return_type == "base64":
            with open(final_path, "rb") as f:
                encoded = base64.b64encode(f.read()).decode("utf-8")
            debug_print("arquivo convertido para base64", base64_length=len(encoded))
            return encoded

        if return_type == "object":
            stat = final_path.stat()
            created_at = datetime.fromtimestamp(stat.st_ctime)
            modified_at = datetime.fromtimestamp(stat.st_mtime)

            return {
                "nome": filename_on_disk,
                "caminho": str(final_path),
                "diretorio": str(final_path.parent),
                "extensao": final_path.suffix,
                "tamanho_bytes": stat.st_size,
                "criado_em": created_at.isoformat(),
                "atualizado_em": modified_at.isoformat(),
                "formato_saida": output_format,
                "caminho_origem": str(source),
            }

        return final_path
