from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from services.api.api_settings_service import AppSettings


def configure_middlewares(app: FastAPI, settings: AppSettings) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allow_origins,
        allow_credentials="*" not in settings.cors_allow_origins,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.add_middleware(
        SessionMiddleware,
        secret_key=settings.session_secret_key,
        session_cookie="sid",
        same_site=settings.session_same_site,
        https_only=settings.session_https_only,
        max_age=settings.session_max_age,
    )
