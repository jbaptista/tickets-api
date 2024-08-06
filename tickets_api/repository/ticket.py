from sqlalchemy.ext.asyncio import AsyncEngine

from tickets_api.database.repository import SqlAlchemyRepositoryMixin
from tickets_api.database.models.ticket import Ticket
from tickets_api.schemas.ticket import TicketCreate


class TicketRepository(SqlAlchemyRepositoryMixin):
    def __init__(self, db_engine: AsyncEngine):
        super().__init__(db_engine)

    async def add_ticket(self, ticket: TicketCreate) -> Ticket:
        ticket = Ticket(**ticket.dict())
        async with self.session() as session:
            session.add(ticket)
            await session.commit()
            return ticket
