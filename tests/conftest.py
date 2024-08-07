from unittest.mock import patch
import pytest
from fastapi.testclient import TestClient
import pytest_asyncio
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker


from tickets_api import config
from tickets_api.app_factory import create_app
from tickets_api.database.models import Base
from tickets_api.services.ticket_service import TicketService
from tickets_api.utils.fastapi import register_state


@pytest_asyncio.fixture
async def async_sqlite_engine():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def app_client(session_factory):
    ticket_service = TicketService(session_factory=session_factory)
    app = create_app(config.Config())
    register_state(app, ticket_service)
    return TestClient(app)


@pytest.fixture
def session_factory(async_sqlite_engine):
    return async_sessionmaker(async_sqlite_engine, expire_on_commit=False)


@pytest_asyncio.fixture
async def session(async_sqlite_engine):
    async_session = async_sessionmaker(async_sqlite_engine, expire_on_commit=False)
    async with async_session() as session:
        yield session


@pytest.fixture
def sync_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        yield session
    Base.metadata.drop_all(engine)
