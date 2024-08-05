from sqlalchemy import select

from tickets_api.database.models import Ticket
from tickets_api.database.models.ticket import Severity


def test_create_ticket(session):
    ticket = Ticket(title="Test Ticket", description=None, severity=Severity.HIGH)
    session.add(ticket)
    session.commit()

    stmt = select(Ticket).where(Ticket.id == ticket.id)
    result = session.execute(stmt).scalar_one()

    assert result.title == "Test Ticket"
    assert result.severity == Severity.HIGH
    assert result.description is None


def test_update_ticket(session):
    ticket = Ticket(title="Test Ticket", description=None, severity=Severity.HIGH)
    session.add(ticket)
    session.commit()

    ticket.title = "Updated Test Ticket"
    session.commit()

    stmt = select(Ticket).where(Ticket.id == ticket.id)
    result = session.execute(stmt).scalar_one()

    assert result.title == "Updated Test Ticket"


def test_get_ticket(session):
    ticket = Ticket(title="Test Ticket", description=None, severity=Severity.HIGH)
    session.add(ticket)
    session.commit()

    stmt = select(Ticket).where(Ticket.id == ticket.id)
    result = session.execute(stmt).scalar_one()

    assert result.title == "Test Ticket"
    assert result.severity == Severity.HIGH
    assert result.description is None


def test_delete_ticket(session):
    ticket = Ticket(title="Test Ticket", description=None, severity=Severity.HIGH)
    session.add(ticket)
    session.commit()

    stmt = select(Ticket).where(Ticket.id == ticket.id)
    result = session.execute(stmt).scalar_one()

    assert result.title == "Test Ticket"
    assert result.severity == Severity.HIGH
    assert result.description is None

    session.delete(ticket)
    session.commit()

    stmt = select(Ticket).where(Ticket.id == ticket.id)
    result = session.execute(stmt).scalar_one_or_none()

    assert result is None
