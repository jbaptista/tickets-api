import pytest
from fastapi.testclient import TestClient
import pytest_asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import create_async_engine


from tickets_api import config
from tickets_api.app_factory import create_app
from tickets_api.database.models import Base
from tickets_api.services.category_service import CategoryService
from tickets_api.services.ticket_service import TicketService
from tickets_api.utils.fastapi import register_state

DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture
async def async_sqlite_engine():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def app_client(async_sqlite_engine):
    ticket_service = TicketService(db_engine=async_sqlite_engine)
    category_service = CategoryService(db_engine=async_sqlite_engine)

    app = create_app(config.Config())
    register_state(app, ticket_service)
    register_state(app, category_service)
    return TestClient(app)


@pytest.fixture
def sync_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        yield session
    Base.metadata.drop_all(engine)
