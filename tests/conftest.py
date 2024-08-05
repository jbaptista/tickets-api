import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


from tickets_api import config
from tickets_api.app_factory import create_app
from tickets_api.database.models import Base


@pytest.fixture
def app_client():
    yield TestClient(
        create_app(
            config.Config(),
        )
    )


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    Base.metadata.drop_all(engine)
