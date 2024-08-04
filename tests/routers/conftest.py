import pytest
from fastapi.testclient import TestClient

from tickets_api import config
from tickets_api.app_factory import create_app


@pytest.fixture
def app_client():
    yield TestClient(
        create_app(
            config.Config(),
        )
    )
