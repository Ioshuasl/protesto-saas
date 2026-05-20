from fastapi import FastAPI

from actions.system.firebird_client import configure_firebird_client
from actions.system.handlers import register_exception_handlers
from actions.system.middlewares import configure_middlewares
from actions.system.request_logging import configure_request_logging
from actions.system.static_files import configure_static_files
from packages.v1.api import api_router
from services.api.api_settings_service import AppSettings


def create_app() -> FastAPI:

    settings = AppSettings.load()
    configure_firebird_client(settings)
    app = FastAPI(title="SAAS Orius")
    register_exception_handlers(
        app, temp_dir=settings.temp_dir, app_env=settings.app_env
    )
    configure_middlewares(app, settings)
    configure_static_files(app, settings)
    configure_request_logging(app, settings.app_config)
    app.include_router(api_router, prefix=settings.app_config.url)

    return app
