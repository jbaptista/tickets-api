import pytest
import httpx


@pytest.mark.asyncio
async def test_healthcheck(app_client):
    app_client_instance = await app_client
    response = app_client_instance.get("/healthcheck")
    assert response.status_code == httpx.codes.OK
    assert response.json() == {"status": "ok"}
