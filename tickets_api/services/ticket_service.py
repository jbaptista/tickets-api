from datetime import datetime

from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.future import select

from tickets_api.database.repository import SqlAlchemyRepositoryMixin
from tickets_api.schemas.ticket import TicketCreate
from tickets_api.database.models.ticket import Ticket


class TicketService(SqlAlchemyRepositoryMixin):
    def __init__(self, db_engine: AsyncEngine):
        super().__init__(db_engine)

    async def create_ticket(self, ticket: TicketCreate) -> Ticket:
        ticket = Ticket(**ticket.dict())
        async with self.session() as session:
            session.add(ticket)
            await session.commit()
            return ticket

    async def get_ticket(self, ticket_id: int) -> Ticket:
        async with self.session() as session:
            return await session.get(Ticket, ticket_id)

    async def get_all_tickets(self) -> list[Ticket]:
        async with self.session() as session:
            result = await session.execute(select(Ticket))
            return result.scalars().all()

    async def delete_ticket(self, ticket_id: int) -> None:
        async with self.session() as session:
            ticket = await session.get(Ticket, ticket_id)
            if not ticket:
                raise HTTPException(status_code=404, detail="Ticket not found")
            await session.delete(ticket)
            await session.commit()

    async def update_ticket(self, ticket_id: int, ticket: TicketCreate) -> Ticket:
        async with self.session() as session:
            ticket_db = await session.get(Ticket, ticket_id)
            if not ticket_db:
                raise HTTPException(status_code=404, detail="Ticket not found")
            ticket_db.title = ticket.title
            ticket_db.description = ticket.description
            ticket_db.severity = ticket.severity
            ticket_db.updated_at = datetime.now()
            await session.commit()
            return ticket_db
