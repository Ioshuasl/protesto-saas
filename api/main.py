import os
import platform
import sys
from pathlib import Path

from starlette.middleware.sessions import SessionMiddleware

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from firebird.driver import driver_config
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from packages.v1.api import api_router
from actions.log.log import Log
from actions.config.config import Config
from actions.system.handlers import register_exception_handlers

if platform.system() == "Windows":
    FB_DIR = r"C:\Program Files\Firebird\Firebird_4_0"
    os.add_dll_directory(FB_DIR)
    driver_config.fb_client_library.value = (
        r"C:\Program Files\Firebird\Firebird_4_0\fbclient.dll"
    )

config = Config.get("app.json")

cors_allow_origins_env = os.getenv("CORS_ALLOW_ORIGINS", "*")
cors_allow_origins = [
    origin.strip() for origin in cors_allow_origins_env.split(",") if origin.strip()
]
if not cors_allow_origins:
    cors_allow_origins = ["*"]

session_same_site = os.getenv("SESSION_SAME_SITE", "lax")
session_https_only = os.getenv("SESSION_HTTPS_ONLY", "false").lower() == "true"
session_max_age = int(os.getenv("SESSION_MAX_AGE", str(60 * 60 * 8)))

app = FastAPI(title="SAAS Orius")
register_exception_handlers(app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_allow_origins,
    allow_credentials="*" not in cors_allow_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    SessionMiddleware,
    secret_key="coloque-uma-secret-bem-grande-e-aleatoria",
    session_cookie="sid",
    same_site=session_same_site,
    https_only=session_https_only,
    max_age=session_max_age,
)


app.mount(path="/temp", app=StaticFiles(directory="./storage/temp"), name="temp")


@app.middleware("http")
async def log_tempo_requisicao(request: Request, call_next):
    log = Log()
    config = Config.get("app.json")

    log_data = {
        "method": request.method,
        "url": str(request.url),
        "headers": dict(request.headers),
    }

    file = Path(config.log.request.path) / config.log.request.name
    log.register(log_data, file)

    response = await call_next(request)
    return response


app.include_router(api_router, prefix=config.url)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=True,
    )
