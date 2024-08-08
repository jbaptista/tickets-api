from fastapi import APIRouter

from tickets_api.schemas.ticket import TicketCreate
from tickets_api.services.ticket_service import TicketService
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


@router.get("")
async def get_all_tickets(ticket_service: TicketService = load_state(TicketService)):
    return await ticket_service.get_all_tickets()


@router.put("/{ticket_id}")
async def update_ticket(
    ticket_id: int,
    ticket: TicketCreate,
    ticket_service: TicketService = load_state(TicketService),
):
    return await ticket_service.update_ticket(ticket_id, ticket)


@router.delete("/{ticket_id}")
async def delete_ticket(
    ticket_id: int, ticket_service: TicketService = load_state(TicketService)
):
    await ticket_service.delete_ticket(ticket_id)
    return {"message": "Ticket deleted"}
