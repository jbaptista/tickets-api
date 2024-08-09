import pytest
from tickets_api.database.models import Ticket
from tickets_api.database.models.category import Category
from tickets_api.database.models.ticket import Severity
from tickets_api.services.ticket_service import TicketService


async def create_categories_in_db(session):
    category_1 = Category(
        name="Test Category 1",
        description="Descriptino Category 1",
        active=True,
        parent_id=None,
    )
    category_2 = Category(
        name="Test Category 2",
        description="Descriptino Category 2",
        active=True,
        parent_id=None,
    )

    session.add_all([category_1, category_2])
    await session.commit()
    await session.refresh(category_1)
    category_2.parent_id = category_1.id
    await session.commit()
    await session.refresh(category_2)
    return [category_1, category_2]


def ticket_1(category_id=None, subcategory_id=None):
    return Ticket(
        title="Test Ticket 1",
        description=None,
        severity=Severity.HIGH,
        category_id=category_id,
        subcategory_id=subcategory_id,
    )


def ticket_2(category_id=None, subcategory_id=None):
    return Ticket(
        title="Test Ticket 2",
        description=None,
        severity=Severity.MEDIUM,
        category_id=category_id,
        subcategory_id=subcategory_id,
    )


async def create_ticket_1_in_db(session):
    [category_1, category_2] = await create_categories_in_db(session)
    ticket1 = ticket_1(category_id=category_1.id, subcategory_id=category_2.id)
    session.add(ticket1)
    await session.commit()
    await session.refresh(ticket1)
    return ticket1


async def create_ticket_2_in_db(session):
    [category_1, category_2] = await create_categories_in_db(session)
    ticket2 = ticket_2(category_id=category_1.id, subcategory_id=category_2.id)
    session.add(ticket2)
    await session.commit()
    await session.refresh(ticket2)
    return ticket2


@pytest.mark.asyncio
async def test_create_ticket(app_client):
    app_client_instance = await app_client
    ticket_service = app_client_instance.app.state.class_registry[TicketService]
    async with ticket_service.session() as session:
        category_1, category_2 = await create_categories_in_db(session)

        response = app_client_instance.post(
            "/tickets",
            json={
                "title": "Test Ticket",
                "description": None,
                "severity": 2,
                "category_id": category_1.id,
                "subcategory_id": category_2.id,
            },
        )

        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Test Ticket"
        assert data["severity"] == 2
        assert data["description"] is None


@pytest.mark.asyncio
async def test_get_ticket(app_client):
    app_client_instance = await app_client
    ticket_service = app_client_instance.app.state.class_registry[TicketService]
    async with ticket_service.session() as session:
        ticket = await create_ticket_1_in_db(session)
        response = app_client_instance.get(f"/tickets/{ticket.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == ticket.title
        assert data["severity"] == ticket.severity.value
        assert data["description"] == ticket.description


@pytest.mark.asyncio
async def test_get_all_tickets(app_client):
    app_client_instance = await app_client
    ticket_service = app_client_instance.app.state.class_registry[TicketService]
    async with ticket_service.session() as session:
        ticket1 = await create_ticket_1_in_db(session)
        ticket2 = await create_ticket_2_in_db(session)
        response = app_client_instance.get("/tickets")
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
async def test_update_ticket(app_client):
    app_client_instance = await app_client
    ticket_service = app_client_instance.app.state.class_registry[TicketService]
    async with ticket_service.session() as session:
        ticket = await create_ticket_1_in_db(session)

        response = app_client_instance.put(
            f"/tickets/{ticket.id}",
            json={
                "title": "Updated Test Ticket",
                "description": None,
                "severity": 2,
                "category_id": ticket.category_id,
                "subcategory_id": ticket.subcategory_id,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Test Ticket"
        assert data["severity"] == 2
        assert data["description"] is None


@pytest.mark.asyncio
async def test_delete_ticket(app_client):
    app_client_instance = await app_client
    ticket_service = app_client_instance.app.state.class_registry[TicketService]
    async with ticket_service.session() as session:
        ticket = await create_ticket_1_in_db(session)

        response = app_client_instance.delete(f"/tickets/{ticket.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Ticket deleted"

        response = app_client_instance.get(f"/tickets/{ticket.id}")
        assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_ticket_with_inexistent_category(app_client):
    app_client_instance = await app_client
    response = app_client_instance.post(
        "/tickets",
        json={
            "title": "Test Ticket",
            "description": None,
            "severity": 2,
            "category_id": 1,
            "subcategory_id": 2,
        },
    )
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Non-existent category"


@pytest.mark.asyncio
async def test_create_ticket_with_inexistent_subcategory(app_client):
    app_client_instance = await app_client
    ticket_service: TicketService = app_client_instance.app.state.class_registry[
        TicketService
    ]
    async with ticket_service.session() as session:
        category_1, category_2 = await create_categories_in_db(session)

        response = app_client_instance.post(
            "/tickets",
            json={
                "title": "Test Ticket",
                "description": None,
                "severity": 2,
                "category_id": category_1.id,
                "subcategory_id": 100,
            },
        )
        assert response.status_code == 400
        data = response.json()
        assert data["detail"] == "Non-existent subcategory"


@pytest.mark.asyncio
async def test_create_ticket_with_inconsistent_categories(app_client):
    app_client_instance = await app_client
    ticket_service: TicketService = app_client_instance.app.state.class_registry[
        TicketService
    ]
    async with ticket_service.session() as session:
        category_1, category_2 = await create_categories_in_db(session)

        response = app_client_instance.post(
            "/tickets",
            json={
                "title": "Test Ticket",
                "description": None,
                "severity": 2,
                "category_id": category_2.id,
                "subcategory_id": category_1.id,
            },
        )
        assert response.status_code == 400
        data = response.json()
        assert data["detail"] == "The subcategory is not a child of the category"


@pytest.mark.asyncio
async def test_create_ticket_issue_high(app_client):
    app_client_instance = await app_client
    ticket_service: TicketService = app_client_instance.app.state.class_registry[
        TicketService
    ]
    async with ticket_service.session() as session:
        category_1, category_2 = await create_categories_in_db(session)

        response = app_client_instance.post(
            "/tickets",
            json={
                "title": "Test Ticket",
                "description": None,
                "severity": Severity.ISSUE_HIGH.value,
                "category_id": category_1.id,
                "subcategory_id": category_2.id,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert (
            data["message"]
            == "Por favor, crie um ticket no link: http://example/fast, a equipe de guardian buscará resolver a sua issue."
        )
        assert data["ticket"]["title"] == "Test Ticket"
        assert data["ticket"]["severity"] == Severity.ISSUE_HIGH.value
        assert data["ticket"]["description"] is None
