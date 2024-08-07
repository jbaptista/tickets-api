import pytest
import httpx
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_healthcheck(app_client: TestClient):
    app_client_instance = await app_client
    response = app_client_instance.get("/healthcheck")
    assert response.status_code == httpx.codes.OK
    assert response.json() == {"status": "ok"}
