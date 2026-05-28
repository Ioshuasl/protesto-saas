from dataclasses import dataclass
from threading import Lock
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from actions.env.env_config_loader import EnvConfigLoader
from database.firebird_host import resolve_firebird_host


@dataclass(frozen=True)
class _FirebirdSettings:
    user: str
    password: str
    host: str
    port: str
    database: str
    charset: str
    pool_pre_ping: bool
    pool_size: int
    max_overflow: int


class Firebird:
    _engine: Optional[Engine] = None
    _engine_lock = Lock()
    _settings: Optional[_FirebirdSettings] = None

    @classmethod
    def _parse_bool(cls, value: object, default: bool = False) -> bool:
        if value is None:
            return default

        if isinstance(value, bool):
            return value

        normalized = str(value).strip().lower()
        if normalized in {"1", "true", "t", "yes", "y", "on"}:
            return True
        if normalized in {"0", "false", "f", "no", "n", "off"}:
            return False
        return default

    @classmethod
    def _parse_int(cls, value: object, field_name: str, default: int) -> int:
        if value in (None, ""):
            return default

        try:
            return int(value)
        except (TypeError, ValueError) as exc:
            raise ValueError(
                f"Configuracao invalida para '{field_name}': {value!r}"
            ) from exc

    @classmethod
    def _require_str(cls, value: object, field_name: str) -> str:
        normalized = "" if value is None else str(value).strip()
        if not normalized:
            raise ValueError(f"Configuracao obrigatoria ausente para '{field_name}'")
        return normalized

    @classmethod
    def _load_settings(cls) -> _FirebirdSettings:
        if cls._settings is not None:
            return cls._settings

        env_database = EnvConfigLoader(".env")

        cls._settings = _FirebirdSettings(
            user=cls._require_str(
                env_database.ORIUS_API_FDB_USER, "ORIUS_API_FDB_USER"
            ),
            password=cls._require_str(
                env_database.ORIUS_API_FDB_PASSWORD,
                "ORIUS_API_FDB_PASSWORD",
            ),
            host=resolve_firebird_host(
                cls._require_str(env_database.ORIUS_API_FDB_HOST, "ORIUS_API_FDB_HOST")
            ),
            port=cls._require_str(
                env_database.ORIUS_API_FDB_PORT, "ORIUS_API_FDB_PORT"
            ),
            database=cls._require_str(
                env_database.ORIUS_API_FDB_NAME, "ORIUS_API_FDB_NAME"
            ),
            charset=cls._require_str(
                env_database.ORIUS_API_FDB_CHARSET,
                "ORIUS_API_FDB_CHARSET",
            ),
            pool_pre_ping=cls._parse_bool(
                env_database.ORIUS_API_FDB_POOL_PRE_PING,
                default=True,
            ),
            pool_size=cls._parse_int(
                env_database.ORIUS_API_FDB_POOL_SIZE,
                field_name="ORIUS_API_FDB_POOL_SIZE",
                default=5,
            ),
            max_overflow=cls._parse_int(
                env_database.ORIUS_API_FDB_POOL_MAX_OVERFLOW,
                field_name="ORIUS_API_FDB_POOL_MAX_OVERFLOW",
                default=10,
            ),
        )
        return cls._settings

    @classmethod
    def _build_dsn(cls, settings: _FirebirdSettings) -> str:
        return (
            f"firebird+firebird://{settings.user}:{settings.password}@"
            f"{settings.host}:{settings.port}/{settings.database}"
        )

    @classmethod
    def _build_engine(cls, settings: _FirebirdSettings) -> Engine:
        return create_engine(
            cls._build_dsn(settings),
            connect_args={"charset": settings.charset},
            pool_pre_ping=settings.pool_pre_ping,
            pool_size=settings.pool_size,
            max_overflow=settings.max_overflow,
        )

    @classmethod
    def get_engine(cls) -> Engine:
        if cls._engine is not None:
            return cls._engine

        with cls._engine_lock:
            if cls._engine is None:
                cls._engine = cls._build_engine(cls._load_settings())

        return cls._engine

    @classmethod
    def dispose(cls):
        with cls._engine_lock:
            if cls._engine:
                cls._engine.dispose()
                cls._engine = None
            cls._settings = None
