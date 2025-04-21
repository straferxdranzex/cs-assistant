from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import get_db
from app.services.ticket import TicketService
from app.services.ai import AIService
from app.api.api_v1.endpoints.tickets import get_current_user

router = APIRouter()


@router.get("/tickets/{ticket_id}/ai-response")
async def get_ai_response(
    ticket_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: Any = Depends(get_current_user),
) -> Any:
    ticket_service = TicketService(db)
    ticket = await ticket_service.get_by_id(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if str(ticket.user_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")

    messages = await ticket_service.get_messages(ticket_id)
    message_history = "\n".join(
        [f"{'AI' if m.is_ai else 'User'}: {m.content}" for m in messages]
    )

    ai_service = AIService()

    async def generate():
        async for chunk in ai_service.generate_response(
            ticket_description=ticket.description,
            message_history=message_history,
            latest_message=messages[-1].content if messages else "",
        ):
            yield f"data: {chunk}\n\n"

    return StreamingResponse(generate(), media_type="text/event-stream")
