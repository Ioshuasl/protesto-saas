import logging
import os
import platform
from pathlib import Path

from firebird.driver import driver_config

from services.api.api_settings_service import AppSettings

logger = logging.getLogger(__name__)

DEFAULT_WINDOWS_FIREBIRD_DIR = r"C:\Program Files\Firebird\Firebird_4_0"
DEFAULT_WINDOWS_FIREBIRD_LIBRARY = str(
    Path(DEFAULT_WINDOWS_FIREBIRD_DIR) / "fbclient.dll"
)


def configure_firebird_client(settings: AppSettings) -> None:
    if platform.system() != "Windows":
        return

    firebird_dir = settings.firebird_client_dir or DEFAULT_WINDOWS_FIREBIRD_DIR
    firebird_library = (
        settings.firebird_client_library or DEFAULT_WINDOWS_FIREBIRD_LIBRARY
    )

    if not Path(firebird_dir).exists():
        logger.warning("Diretorio do client Firebird nao encontrado: %s", firebird_dir)
        return

    os.add_dll_directory(firebird_dir)

    if not Path(firebird_library).exists():
        logger.warning(
            "Biblioteca do client Firebird nao encontrada: %s", firebird_library
        )
        return

    driver_config.fb_client_library.value = firebird_library
