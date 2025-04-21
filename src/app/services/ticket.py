from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.ticket import Ticket, Message
from app.schemas.ticket import TicketCreate, TicketUpdate, MessageCreate


class TicketService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_id(self, ticket_id: str) -> Optional[Ticket]:
        result = await self.db.execute(select(Ticket).where(Ticket.id == ticket_id))
        return result.scalar_one_or_none()

    async def get_user_tickets(self, user_id: str) -> List[Ticket]:
        result = await self.db.execute(select(Ticket).where(Ticket.user_id == user_id))
        return result.scalars().all()

    async def create(self, ticket_in: TicketCreate, user_id: str) -> Ticket:
        db_ticket = Ticket(**ticket_in.model_dump(), user_id=user_id)
        self.db.add(db_ticket)
        await self.db.commit()
        await self.db.refresh(db_ticket)
        return db_ticket

    async def update(self, ticket: Ticket, ticket_in: TicketUpdate) -> Ticket:
        update_data = ticket_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(ticket, field, value)
        await self.db.commit()
        await self.db.refresh(ticket)
        return ticket

    async def add_message(
        self, ticket_id: str, message_in: MessageCreate, is_ai: bool = False
    ) -> Message:
        db_message = Message(
            **message_in.model_dump(), ticket_id=ticket_id, is_ai=is_ai
        )
        self.db.add(db_message)
        await self.db.commit()
        await self.db.refresh(db_message)
        return db_message

    async def get_messages(self, ticket_id: str) -> List[Message]:
        result = await self.db.execute(
            select(Message).where(Message.ticket_id == ticket_id)
        )
        return result.scalars().all()
