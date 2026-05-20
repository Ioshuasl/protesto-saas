from __future__ import annotations

from functools import lru_cache

from actions.env.env_config_loader import EnvConfigLoader


def _parse_bool(value: object, default: bool = False) -> bool:
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


@lru_cache(maxsize=1)
def use_orm_firebird() -> bool:
    """Lê USE_ORM_FIREBIRD do .env (default: false)."""
    env = EnvConfigLoader(".env")
    return _parse_bool(getattr(env, "USE_ORM_FIREBIRD", None), default=False)
