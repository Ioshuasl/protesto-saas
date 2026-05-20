import importlib
import pkgutil
import re
from functools import lru_cache
from typing import Type, TypeVar
from actions.env.env_config_loader import EnvConfigLoader

T = TypeVar("T")


class ServiceFactory:

    def __init__(self):
        env = EnvConfigLoader(".env")
        self.base_root = "packages.v1"
        self.current_state = env.ORIUS_CLIENT_STATE

    @lru_cache(maxsize=64)
    def make(self, class_name: str, interface: Type[T]) -> T:

        module_name = re.sub(r"(?<!^)(?=[A-Z])", "_", class_name).lower()

        # Varre dinamicamente todos os subpacotes
        base_module = importlib.import_module(self.base_root)

        for finder, name, ispkg in pkgutil.walk_packages(
            base_module.__path__, prefix=f"{self.base_root}."
        ):
            if ".services." in name and name.endswith(
                f".{self.current_state}.{module_name}"
            ):
                module = importlib.import_module(name)

                if hasattr(module, class_name):
                    clazz = getattr(module, class_name)

                    if not issubclass(clazz, interface):
                        raise TypeError(
                            f"{class_name} não implementa {interface.__name__}"
                        )

                    return clazz()

        raise ImportError(
            f"Serviço '{class_name}' não encontrado para o estado '{self.current_state}'."
        )
