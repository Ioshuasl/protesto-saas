# ged_locator.py
import re
from pathlib import Path
from typing import Iterable, Optional

from packages.v1.ged.actions.ged_base import GedBase


class GedLocator(GedBase):
    def candidate_dirs(
        self,
        serventia: str,
        record_id: int,
        pasta: Optional[str],
        include_deleted: bool,
    ) -> Iterable[Path]:
        yield self.build_base_path(serventia, record_id, pasta, deleted=False)

        if include_deleted:
            yield self.build_base_path(serventia, record_id, pasta, deleted=True)

    @staticmethod
    def _matches_exact_record_id(path: Path, record_id: int, filename_contains: str) -> bool:
        stem = path.stem

        contains = (filename_contains or "").strip()
        if contains and contains not in stem:
            return False

        target = str(int(record_id))
        for token in re.findall(r"\d+", stem):
            if str(int(token)) == target:
                return True

        return False

    def locate(
        self,
        serventia: str,
        record_id: int,
        filename_contains: str = "",
        pasta: Optional[str] = None,
        extensions: Iterable[str] | None = None,
        include_deleted: bool = False,
    ) -> Optional[Path]:
        extensions = extensions or ["tif", "pdf", "jpg"]

        for base in self.candidate_dirs(serventia, record_id, pasta, include_deleted):
            if not base.exists():
                continue

            for ext in extensions:
                for file in sorted(base.glob(f"*.{ext}")):
                    if self._matches_exact_record_id(file, int(record_id), filename_contains):
                        return file

        return None
