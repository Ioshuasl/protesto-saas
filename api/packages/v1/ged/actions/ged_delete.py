# ged_delete.py
import os
from pathlib import Path
from dataclasses import dataclass

from packages.v1.ged.actions.ged_base import GedBase


@dataclass
class GedDeleteResult:
    original: Path
    deleted: Path
    backed_up: bool


class GedDelete(GedBase):
    def move_with_backup(self, src: Path, dest: Path) -> bool:
        dest.parent.mkdir(parents=True, exist_ok=True)

        backed_up = False
        if dest.exists():
            backup = dest.with_suffix(dest.suffix + ".bak")
            os.replace(dest, backup)
            backed_up = True

        os.replace(src, dest)
        return backed_up

    def execute(
        self,
        serventia: str,
        record_id: int,
        filename: str,
        pasta: str | None = None,
    ) -> GedDeleteResult:
        self.validate_filename(filename)

        src_dir = self.build_base_path(serventia, record_id, pasta, deleted=False)
        dest_dir = self.build_base_path(serventia, record_id, pasta, deleted=True)

        src = src_dir / filename
        dest = dest_dir / filename

        if not src.exists():
            raise FileNotFoundError(src)

        backed_up = self.move_with_backup(src, dest)

        return GedDeleteResult(
            original=src,
            deleted=dest,
            backed_up=backed_up,
        )
