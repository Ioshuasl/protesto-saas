from contextlib import contextmanager
from typing import Any, Generator

from database.firebird import Firebird
from packages.v1.pyros.exceptions.errors import PyrosTransactionError


class TransactionManager:
    @contextmanager
    def transaction(self) -> Generator[Any, None, None]:
        try:
            engine = Firebird.get_engine()
            with engine.begin() as connection:
                yield connection
        except Exception as exc:
            raise PyrosTransactionError("Falha ao iniciar transacao Pyros") from exc
