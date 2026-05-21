from __future__ import annotations

from functools import lru_cache

from actions.env.env_config_loader import EnvConfigLoader

# development → login sem 2FA (apenas email + senha)
_DEVELOPMENT_ENVS = frozenset({"dev", "development", "local"})

# production → login com 2FA obrigatório (n8n)
_PRODUCTION_ENVS = frozenset({"prod", "production"})


@lru_cache(maxsize=1)
def get_api_env() -> str:
    """Valor normalizado de API_ENV (.env). Vazio se não definido."""
    try:
        env = EnvConfigLoader(".env").API_ENV
    except AttributeError:
        return ""
    return str(env or "").strip().lower()


@lru_cache(maxsize=1)
def is_api_development() -> bool:
    """True quando API_ENV=development (ou dev/local). Bypass de 2FA no authenticate."""
    return get_api_env() in _DEVELOPMENT_ENVS


@lru_cache(maxsize=1)
def is_api_production() -> bool:
    """True quando API_ENV=production (ou prod). 2FA obrigatório no authenticate."""
    return get_api_env() in _PRODUCTION_ENVS
