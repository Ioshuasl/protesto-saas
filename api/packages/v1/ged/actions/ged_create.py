# packages/v1/ged/actions/ged_create.py
import base64
import os
from pathlib import Path
from typing import List, Optional

from PIL import Image, ImageSequence
import fitz  # PyMuPDF

from actions.env.env_config_loader import EnvConfigLoader
from packages.v1.ged.actions.ged_base import GedBase
from packages.v1.ged.actions.ged_filename_builder import GedFilenameBuilder


class GedCreate(GedBase):
    def __init__(self, base_dir: Optional[str | Path | None] = None):
        env = EnvConfigLoader(env_file=".env")
        print(f"ORIUS_GED: {getattr(env, 'ORIUS_GED', None)}")

        default_base = getattr(env, "GED_BASE_DIR", None) or getattr(env, "ORIUS_GED", None)
        super().__init__(base_dir or default_base)

    def decode_base64(self, data: str) -> bytes:
        if not isinstance(data, str) or not data.strip():
            raise ValueError("Base64 vazio ou invalido")

        s = data.strip()
        if "base64," in s:
            s = s.split("base64,", 1)[1]

        s = "".join(s.split())
        pad = (-len(s)) % 4
        if pad:
            s += "=" * pad

        return base64.b64decode(s, validate=False)

    def images_from_pdf(self, pdf_bytes: bytes, dpi: int) -> List[Image.Image]:
        images: List[Image.Image] = []

        zoom = dpi / 72.0
        matrix = fitz.Matrix(zoom, zoom)

        with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
            for page in doc:
                pix = page.get_pixmap(matrix=matrix, alpha=False)
                img = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
                images.append(img)

        if not images:
            raise RuntimeError("PDF convertido, mas nenhuma pagina foi gerada")

        return images

    def atomic_save(
        self,
        target: Path,
        images: List[Image.Image],
        quality: dict,
    ) -> None:
        if not images:
            raise ValueError("Nenhuma imagem para salvar")

        tmp = target.with_name(f".{target.name}.tmp")
        pages_to_save: List[Image.Image] = []

        if target.exists():
            with Image.open(target) as existing_tiff:
                for frame in ImageSequence.Iterator(existing_tiff):
                    pages_to_save.append(frame.copy())

        pages_to_save.extend(images)

        save_kwargs = {
            "save_all": True,
            "append_images": pages_to_save[1:],
            "format": "TIFF",
        }

        if quality:
            save_kwargs.update(quality)

        pages_to_save[0].save(tmp, **save_kwargs)
        os.replace(tmp, target)

    def execute(
        self,
        serventia: int,
        record_id: int,
        filename: str | None,
        base64_data: str,
        pasta: str | int | None = None,
        quality: dict | None = None,
    ) -> Path:
        subtipo = pasta

        pasta_dir: str | None = None
        if isinstance(pasta, str):
            pasta_dir = pasta.strip() or None

        if not filename:
            if not serventia:
                raise ValueError("serventia e obrigatorio para gerar o nome do arquivo")

            filename = GedFilenameBuilder.build(
                serventia=serventia,
                subtipo=subtipo,
                record_id=record_id,
            )

        self.validate_filename(filename)

        target_dir = self.build_base_path(serventia, record_id, pasta_dir)
        target_dir.mkdir(parents=True, exist_ok=True)

        target = target_dir / filename

        raw = self.decode_base64(base64_data)

        dpi = (quality or {}).get("dpi", 300)
        if isinstance(dpi, tuple):
            dpi = dpi[0]

        images = self.images_from_pdf(raw, dpi=dpi)

        self.atomic_save(target, images, quality or {})

        return target
