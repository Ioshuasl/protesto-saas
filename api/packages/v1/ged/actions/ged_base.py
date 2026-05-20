# ged_base.py
from pathlib import Path
from typing import Optional


class GedSecurityError(ValueError):
    pass


class GedBase:
    def __init__(self, base_dir: str | Path):
        self.base_dir = Path(base_dir).resolve()

    # -------------------------
    # Validações
    # -------------------------

    @staticmethod
    def validate_folder_segment(value: str, field: str):
        if not value:
            raise ValueError(f"{field} não pode ser vazio")

        if "/" in value or "\\" in value or ".." in value:
            raise GedSecurityError(f"{field} inválido")

    @staticmethod
    def validate_filename(filename: str):
        if not filename:
            raise ValueError("filename não pode ser vazio")

        # garante que não exista path embutido
        if Path(filename).name != filename:
            raise GedSecurityError("filename contém path inválido")

        if ".." in filename:
            raise GedSecurityError("filename inválido")

    # -------------------------
    # Utilidades
    # -------------------------

    @staticmethod
    def faixa(record_id: int) -> str:
        return str(record_id // 1000).zfill(3)

    def ensure_inside_base(self, path: Path):
        resolved = path.resolve()
        if not str(resolved).startswith(str(self.base_dir)):
            raise GedSecurityError("Path fora do diretório base")
        return resolved

    def build_base_path(
        self,
        serventia: str | int,
        record_id: int,
        pasta: Optional[str] = None,
        deleted: bool = False,
    ) -> Path:

        # -------------------------
        # normalização obrigatória
        # -------------------------

        serventia_id = int(serventia)

        serventia_dir = {
            1: "Spd_Tab",
            2: "Spd_Civ",
            3: "Spd_Pro",
            4: "Spd_Rtd",
            5: "Spd_Reg",
        }.get(serventia_id, str(serventia_id))

        self.validate_folder_segment(serventia_dir, "serventia")
        if pasta:
            self.validate_folder_segment(pasta, "pasta")

        # padrão legado: base/(Retirados)/serventia/(pasta)/faixa
        parts = [
            self.base_dir,
            "Retirados" if deleted else "",
            serventia_dir,
        ]

        if pasta:
            parts.append(pasta)

        parts.append(self.faixa(record_id))

        path = Path(*[p for p in parts if p])
        return self.ensure_inside_base(path)
