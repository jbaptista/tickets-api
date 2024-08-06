from fastapi import APIRouter

from tickets_api.schemas.ticket import TicketCreate
from tickets_api.services.ticket import TicketService
from tickets_api.utils.fastapi import load_state

router = APIRouter()


@router.post("")
async def create_ticket(
    ticket: TicketCreate, ticket_service: TicketService = load_state(TicketService)
):
    return await ticket_service.create_ticket(ticket)


@router.get("/{ticket_id}")
async def get_ticket(
    ticket_id: int, ticket_service: TicketService = load_state(TicketService)
):
    return await ticket_service.get_ticket(ticket_id)
