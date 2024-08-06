from sqlalchemy.ext.asyncio import AsyncEngine

from tickets_api.schemas.ticket import TicketCreate
from tickets_api.repository.ticket import TicketRepository


class TicketService:
    def __init__(self, db_engine: AsyncEngine):
        self.ticket_repository = TicketRepository(db_engine)

    async def create_ticket(self, ticket: TicketCreate):
        return await self.ticket_repository.add_ticket(ticket)
