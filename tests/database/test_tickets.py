from sqlalchemy import select

from tickets_api.database.models import Ticket
from tickets_api.database.models.ticket import Severity


def test_create_ticket(sync_session):
    ticket = Ticket(
        title="Test Ticket",
        description=None,
        severity=Severity.HIGH,
        category_id=1,
        subcategory_id=2,
    )
    sync_session.add(ticket)
    sync_session.commit()

    stmt = select(Ticket).where(Ticket.id == ticket.id)
    result = (sync_session.execute(stmt)).scalar_one()

    assert result.title == "Test Ticket"
    assert result.severity == Severity.HIGH
    assert result.description is None


def test_update_ticket(sync_session):
    ticket = Ticket(
        title="Test Ticket",
        description=None,
        severity=Severity.HIGH,
        category_id=1,
        subcategory_id=2,
    )
    sync_session.add(ticket)
    sync_session.commit()

    ticket.title = "Updated Test Ticket"
    sync_session.commit()

    stmt = select(Ticket).where(Ticket.id == ticket.id)
    result = (sync_session.execute(stmt)).scalar_one()

    assert result.title == "Updated Test Ticket"


def test_get_ticket(sync_session):
    ticket = Ticket(
        title="Test Ticket",
        description=None,
        severity=Severity.HIGH,
        category_id=1,
        subcategory_id=2,
    )
    sync_session.add(ticket)
    sync_session.commit()

    stmt = select(Ticket).where(Ticket.id == ticket.id)
    result = (sync_session.execute(stmt)).scalar_one()

    assert result.title == "Test Ticket"
    assert result.severity == Severity.HIGH
    assert result.description is None


def test_delete_ticket(sync_session):
    ticket = Ticket(
        title="Test Ticket",
        description=None,
        severity=Severity.HIGH,
        category_id=1,
        subcategory_id=2,
    )
    sync_session.add(ticket)
    sync_session.commit()

    stmt = select(Ticket).where(Ticket.id == ticket.id)
    result = (sync_session.execute(stmt)).scalar_one()

    assert result.title == "Test Ticket"
    assert result.severity == Severity.HIGH
    assert result.description is None

    sync_session.delete(ticket)
    sync_session.commit()

    stmt = select(Ticket).where(Ticket.id == ticket.id)
    result = (sync_session.execute(stmt)).scalar_one_or_none()

    assert result is None


def test_get_all_tickets(sync_session):
    ticket1 = Ticket(
        title="Test Ticket 1",
        description=None,
        severity=Severity.HIGH,
        category_id=1,
        subcategory_id=2,
    )
    ticket2 = Ticket(
        title="Test Ticket 2",
        description=None,
        severity=Severity.MEDIUM,
        category_id=1,
        subcategory_id=2,
    )
    sync_session.add_all([ticket1, ticket2])
    sync_session.commit()

    stmt = select(Ticket)
    result = (sync_session.execute(stmt)).scalars().all()

    assert len(result) == 2
    assert result[0].title == "Test Ticket 1"
    assert result[0].severity == Severity.HIGH
    assert result[0].description is None
    assert result[1].title == "Test Ticket 2"
    assert result[1].severity == Severity.MEDIUM
    assert result[1].description is None


def test_get_ticket_not_found(sync_session):
    stmt = select(Ticket).where(Ticket.id == 1)
    result = (sync_session.execute(stmt)).scalar_one_or_none()

    assert result is None
