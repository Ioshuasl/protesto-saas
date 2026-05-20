import importlib
from actions.config.config import Config
from typing import Optional, Any, Type


class DynamicImport:

    def __init__(self) -> None:
        self.config: dict[str, Any] = Config.get("app.json")
        self.base: str = "packages.v1"
        self.package: Optional[str] = None
        self.table: Optional[str] = None

    def set_package(self, name: str) -> None:
        self.package = name

    def set_table(self, table: str):
        self.table = table

    def service(self, name: str, class_name: str) -> Type[Any]:
        try:
            # Define o nome do Módulo
            module_file = f"{name}"
            # Define o caminho do arquivo
            path = f"{self.base}.{self.package}.services.{self.table}.{self.config.state}.{module_file}"
            # Realiza a importação do arquivo
            module = importlib.import_module(path)
            clazz = getattr(module, class_name)
            return clazz
        except (ImportError, AttributeError) as e:
            raise ImportError(f"Erro ao importar '{class_name}' de '{path}': {e}")
