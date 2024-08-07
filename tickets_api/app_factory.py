from fastapi import FastAPI

from .config import Config
from .routers.healthcheck import router as healthcheck_router
from .routers.tickets import router as tickets_router

from .database.repository import make_session_factory
from .utils.fastapi import register_state
from .services.ticket_service import TicketService


def create_app(config: Config) -> FastAPI:
    app = FastAPI()

    session_factory = make_session_factory(config.database.url)

    ticket_service = TicketService(session_factory)
    register_state(app, ticket_service)

    app.include_router(healthcheck_router, prefix="/healthcheck")
    app.include_router(tickets_router, prefix="/ticket")

    return app
