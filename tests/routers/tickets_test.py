import pytest
from fastapi.testclient import TestClient
from tickets_api.database.models import Ticket
from tickets_api.database.models.ticket import Severity
from tickets_api.services.ticket_service import TicketService


@pytest.fixture
def ticket_1():
    return Ticket(title="Test Ticket 1", description=None, severity=Severity.HIGH)


@pytest.fixture
def ticket_2():
    return Ticket(title="Test Ticket 2", description=None, severity=Severity.MEDIUM)


@pytest.fixture()
async def create_ticket_1_in_db(app_client, ticket_1: Ticket):
    ticket_service: TicketService = app_client.app.state.class_registry[TicketService]
    async with ticket_service.session() as session:
        session.add(ticket_1)
        await session.commit()
        await session.refresh(ticket_1)
        return ticket_1


@pytest.fixture
async def create_ticket_2_in_db(app_client, ticket_2: Ticket):
    ticket_service: TicketService = app_client.app.state.class_registry[TicketService]
    async with ticket_service.session() as session:
        session.add(ticket_2)
        await session.commit()
        await session.refresh(ticket_2)
        return ticket_2


@pytest.mark.asyncio
async def test_create_ticket(app_client: TestClient):
    response = app_client.post(
        "/ticket",
        json={"title": "Test Ticket", "description": None, "severity": 2},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Ticket"
    assert data["severity"] == 2
    assert data["description"] is None


@pytest.mark.asyncio
async def test_get_ticket(app_client: TestClient, create_ticket_1_in_db):
    ticket = await create_ticket_1_in_db
    response = app_client.get(f"/ticket/{ticket.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == ticket.title
    assert data["severity"] == ticket.severity.value
    assert data["description"] == ticket.description


@pytest.mark.asyncio
async def test_get_all_tickets(
    app_client: TestClient, create_ticket_1_in_db, create_ticket_2_in_db
):
    ticket1 = await create_ticket_1_in_db
    ticket2 = await create_ticket_2_in_db
    response = app_client.get("/ticket")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["title"] == ticket1.title
    assert data[0]["severity"] == ticket1.severity.value
    assert data[0]["description"] == ticket1.description
    assert data[1]["title"] == ticket2.title
    assert data[1]["severity"] == ticket2.severity.value
    assert data[1]["description"] == ticket2.description


@pytest.mark.asyncio
async def test_update_ticket(app_client: TestClient, create_ticket_1_in_db):
    ticket = await create_ticket_1_in_db
    response = app_client.put(
        f"/ticket/{ticket.id}",
        json={"title": "Updated Test Ticket", "description": None, "severity": 2},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Test Ticket"
    assert data["severity"] == 2
    assert data["description"] is None


@pytest.mark.asyncio
async def test_delete_ticket(app_client: TestClient, create_ticket_1_in_db):
    ticket = await create_ticket_1_in_db
    response = app_client.delete(f"/ticket/{ticket.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Ticket deleted"
    response = app_client.get(f"/ticket/{ticket.id}")
    assert response.status_code == 404
