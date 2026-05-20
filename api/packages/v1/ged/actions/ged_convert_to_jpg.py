import base64
from pathlib import Path
from typing import Optional, Literal

from actions.env.env_config_loader import EnvConfigLoader
from packages.v1.ged.actions.ged_base import GedBase
from packages.v1.ged.actions.ged_convert import GEDConvert, ReturnType


class GEDConvertToJpg(GedBase):
    """
    Converte arquivos SPD/TIF multipagina para JPG
    e grava exclusivamente no diretorio informado.

    Tipos de retorno:
      - path: caminho relativo completo (default)
      - filename: somente o nome do arquivo
      - base64: conteudo do arquivo em base64
    """

    def __init__(self, base_dir: Optional[str | Path | None] = None):
        env = EnvConfigLoader(env_file=".env")

        default_base = getattr(env, "GED_BASE_DIR", None) or getattr(
            env, "ORIUS_GED", None
        )

        super().__init__(base_dir or default_base)
        self._converter = GEDConvert(self.base_dir)

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
        page_position: Literal["first", "last"] = "first",
    ):
        return self._converter.convert(
            serventia=serventia,
            record_id=record_id,
            pasta=pasta,
            filename_contains=filename_contains,
            quality=quality,
            output_dir=output_dir,
            temp_dir=temp_dir,
            return_type=return_type,
            page_position=page_position,
            output_format="jpg",
        )
