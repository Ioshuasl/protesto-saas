import os
from dataclasses import dataclass
from pathlib import Path
from types import SimpleNamespace

from actions.config.config import Config


@dataclass(frozen=True)
class AppSettings:
    app_config: SimpleNamespace
    app_env: str
    cors_allow_origins: list[str]
    session_same_site: str
    session_https_only: bool
    session_max_age: int
    session_secret_key: str
    temp_dir: Path
    firebird_client_dir: str | None
    firebird_client_library: str | None

    @classmethod
    def load(cls) -> "AppSettings":
        app_config = Config.get("app.json")
        app_env = os.getenv("APP_ENV", "development").strip().lower() or "development"

        cors_allow_origins_env = os.getenv("CORS_ALLOW_ORIGINS", "*")
        cors_allow_origins = [
            origin.strip()
            for origin in cors_allow_origins_env.split(",")
            if origin.strip()
        ] or ["*"]

        session_secret_key = os.getenv("SESSION_SECRET_KEY", "").strip()
        if not session_secret_key:
            if app_env in {"prod", "production"}:
                raise ValueError(
                    "SESSION_SECRET_KEY obrigatoria em ambiente de producao"
                )
            session_secret_key = "dev-session-secret-change-me"

        project_root = Path(__file__).resolve().parents[1]
        temp_dir = project_root / "storage" / "temp"

        return cls(
            app_config=app_config,
            app_env=app_env,
            cors_allow_origins=cors_allow_origins,
            session_same_site=os.getenv("SESSION_SAME_SITE", "lax"),
            session_https_only=os.getenv("SESSION_HTTPS_ONLY", "false").strip().lower()
            == "true",
            session_max_age=int(os.getenv("SESSION_MAX_AGE", str(60 * 60 * 8))),
            session_secret_key=session_secret_key,
            temp_dir=temp_dir,
            firebird_client_dir=os.getenv("FIREBIRD_CLIENT_DIR", "").strip() or None,
            firebird_client_library=os.getenv("FIREBIRD_CLIENT_LIBRARY", "").strip()
            or None,
        )
