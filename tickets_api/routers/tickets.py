from fastapi import APIRouter
from loguru import logger

from tickets_api.schemas.ticket import TicketCreate
from tickets_api.services.ticket_service import TicketService
from tickets_api.utils.fastapi import load_state


router = APIRouter()


@router.post("")
async def create_ticket(
    ticket: TicketCreate, ticket_service: TicketService = load_state(TicketService)
):
    result = await ticket_service.create_ticket(ticket)
    logger.info(f"Ticket created: {result}")
    return result


@router.get("/{ticket_id}")
async def get_ticket(
    ticket_id: int, ticket_service: TicketService = load_state(TicketService)
):
    result = await ticket_service.get_ticket(ticket_id)
    logger.info(f"Ticket {ticket_id} found")
    return result


@router.get("")
async def get_all_tickets(ticket_service: TicketService = load_state(TicketService)):
    result = await ticket_service.get_all_tickets()
    logger.info("All tickets returned")
    return result


@router.put("/{ticket_id}")
async def update_ticket(
    ticket_id: int,
    ticket: TicketCreate,
    ticket_service: TicketService = load_state(TicketService),
):
    result = await ticket_service.update_ticket(ticket_id, ticket)
    logger.info(f"Ticket {ticket_id} updated")
    return result


@router.delete("/{ticket_id}")
async def delete_ticket(
    ticket_id: int, ticket_service: TicketService = load_state(TicketService)
):
    await ticket_service.delete_ticket(ticket_id)
    logger.info(f"Ticket {ticket_id} deleted")
    return {"message": "Ticket deleted"}
