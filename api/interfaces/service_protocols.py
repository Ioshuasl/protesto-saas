from typing import Protocol, Any, runtime_checkable


@runtime_checkable
class ServiceProtocolsInterface(Protocol):
    """
    Contrato que garante que todo serviço tenha um método execute.
    """

    def execute(self, schema: Any) -> Any: ...
