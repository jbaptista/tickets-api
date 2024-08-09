from datetime import datetime

from fastapi import HTTPException

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncEngine

from tickets_api.database.repository import SqlAlchemyRepositoryMixin
from tickets_api.schemas.ticket import Severity, TicketCreate
from tickets_api.database.models.ticket import Ticket
from tickets_api.database.models.category import Category


class TicketService(SqlAlchemyRepositoryMixin):
    def __init__(self, db_engine: AsyncEngine):
        super().__init__(db_engine)

    async def create_ticket(self, ticket: TicketCreate):
        async with self.session() as session:
            await self.validate_category_and_subcategory(
                session, ticket.category_id, ticket.subcategory_id
            )

            new_ticket = Ticket(**ticket.model_dump())
            session.add(new_ticket)
            await session.commit()
            if new_ticket.severity == Severity.ISSUE_HIGH:
                return {
                    "ticket": new_ticket,
                    "message": "Por favor, crie um ticket no link: http://example/fast, a equipe de guardian buscará resolver a sua issue.",
                }
            return new_ticket

    async def get_ticket(self, ticket_id: int) -> Ticket:
        async with self.session() as session:
            ticket = await session.get(Ticket, ticket_id)
            if not ticket:
                raise HTTPException(status_code=404, detail="Ticket not found")
            return ticket

    async def get_all_tickets(self) -> list[Ticket]:
        async with self.session() as session:
            stmt = select(Ticket)
            result = await session.execute(stmt)
            return list(result.scalars().all())

    async def delete_ticket(self, ticket_id: int) -> None:
        async with self.session() as session:
            ticket = await session.get(Ticket, ticket_id)
            if not ticket:
                raise HTTPException(status_code=404, detail="Ticket not found")
            await session.delete(ticket)
            await session.commit()

    async def update_ticket(self, ticket_id: int, ticket: TicketCreate) -> Ticket:
        async with self.session() as session:
            ticket_db: Ticket | None = await session.get(Ticket, ticket_id)
            if not ticket_db:
                raise HTTPException(status_code=404, detail="Ticket not found")
            ticket_db.title = ticket.title
            if ticket.description:
                ticket_db.description = ticket.description
            ticket_db.severity = ticket.severity
            ticket_db.updated_at = datetime.now()
            await session.commit()
            return ticket_db

    async def validate_category_and_subcategory(
        self, session, category_id, subcategory_id
    ):
        category = await session.get(Category, category_id)
        if not category:
            raise HTTPException(status_code=400, detail="Non-existent category")
        subcategory = await session.get(Category, subcategory_id)
        if not subcategory:
            raise HTTPException(status_code=400, detail="Non-existent subcategory")
        if subcategory.parent_id != category_id:
            raise HTTPException(
                status_code=400, detail="The subcategory is not a child of the category"
            )
        return category, subcategory
