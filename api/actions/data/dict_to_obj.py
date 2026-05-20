from typing import Any, Mapping, Iterable


class DictToObj:
    """
    Converte dicts (aninhados) em objetos com acesso por ponto.
    - d["x"] -> o.x
    - Listas/tuplas são convertidas recursivamente.
    - Mantém método parse() para voltar ao dict original.
    """

    __slots__ = ("__data__",)

    def __init__(self, data: Mapping[str, Any] | None = None):
        object.__setattr__(self, "__data__", {})
        if data:
            for k, v in data.items():
                self.__data__[k] = self._convert(v)

    # ===== Conversões =====
    @classmethod
    def _convert(cls, value: Any) -> Any:
        if isinstance(value, Mapping):
            return cls(value)
        if isinstance(value, list):
            return [cls._convert(v) for v in value]
        if isinstance(value, tuple):
            return tuple(cls._convert(v) for v in value)
        return value

    def parse(self) -> dict[str, Any]:
        def back(v: Any) -> Any:
            if isinstance(v, DictToObj):
                return v.parse()
            if isinstance(v, list):
                return [back(i) for i in v]
            if isinstance(v, tuple):
                return tuple(back(i) for i in v)
            return v

        return {k: back(v) for k, v in self.__data__.items()}

    # ===== Acesso por ponto / item =====
    def __getattr__(self, name: str) -> Any:
        try:
            return self.__data__[name]
        except KeyError as e:
            raise AttributeError(name) from e

    def __setattr__(self, name: str, value: Any) -> None:
        # protege o atributo interno
        if name == "__data__":
            object.__setattr__(self, name, value)
        else:
            self.__data__[name] = self._convert(value)

    def __getitem__(self, key: str) -> Any:
        return self.__data__[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.__data__[key] = self._convert(value)

    def __contains__(self, key: str) -> bool:
        return key in self.__data__

    def keys(self) -> Iterable[str]:
        return self.__data__.keys()

    def items(self) -> Iterable[tuple[str, Any]]:
        return self.__data__.items()

    def values(self) -> Iterable[Any]:
        return self.__data__.values()

    def __iter__(self):
        return iter(self.__data__)

    def __len__(self) -> int:
        return len(self.__data__)

    def __repr__(self) -> str:
        return f"DictToObj({self.__data__!r})"
