from fastapi import FastAPI

from .config import Config
from .routers.healthcheck import router as healthcheck_router


def create_app(config: Config) -> FastAPI:
    app = FastAPI()

    app.include_router(healthcheck_router, prefix="/healthcheck")

    return app
