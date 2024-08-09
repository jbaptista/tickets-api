from fastapi import FastAPI
from loguru import logger
from fastapi.responses import JSONResponse
from tickets_api.services.category_service import CategoryService

from .config import Config
from .routers.healthcheck import router as healthcheck_router
from .routers.tickets import router as tickets_router
from .routers.categories import router as category_router

from .database.repository import make_db_engine
from .utils.fastapi import register_state
from .services.ticket_service import TicketService


def create_app(config: Config) -> FastAPI:
    app = FastAPI()

    db_engine = make_db_engine(config.database.url)

    ticket_service = TicketService(db_engine)
    register_state(app, ticket_service)
    category_service = CategoryService(db_engine)
    register_state(app, category_service)

    app.include_router(healthcheck_router, prefix="/healthcheck")
    app.include_router(tickets_router, prefix="/tickets")
    app.include_router(category_router, prefix="/categories")

    @app.exception_handler(Exception)
    async def handle_exception(request, exc):
        logger.exception(exc)
        return JSONResponse(
            status_code=500,
            content={"message": "Internal server error"},
        )

    return app
