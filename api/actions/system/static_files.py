from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from services.api.api_settings_service import AppSettings


def configure_static_files(app: FastAPI, settings: AppSettings) -> None:
    settings.temp_dir.mkdir(parents=True, exist_ok=True)
    app.mount(
        path="/temp", app=StaticFiles(directory=str(settings.temp_dir)), name="temp"
    )
