import httpx
from fastapi.testclient import TestClient


def test_healthcheck(app_client: TestClient):
    response = app_client.get("/healthcheck")
    assert response.status_code == httpx.codes.OK
    assert response.json() == {"status": "ok"}
