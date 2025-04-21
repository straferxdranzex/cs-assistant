from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.session import get_db
from app.schemas.ticket import (
    Ticket,
    TicketCreate,
    TicketUpdate,
    Message,
    MessageCreate,
)
from app.services.ticket import TicketService
from app.services.user import UserService

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")


async def get_current_user(
    db: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> Any:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user_service = UserService(db)
    user = await user_service.get_by_id(user_id)
    if user is None:
        raise credentials_exception
    return user


@router.get("/", response_model=List[Ticket])
async def list_tickets(
    db: AsyncSession = Depends(get_db), current_user: Any = Depends(get_current_user)
) -> Any:
    ticket_service = TicketService(db)
    return await ticket_service.get_user_tickets(str(current_user.id))


@router.post("/", response_model=Ticket)
async def create_ticket(
    *,
    db: AsyncSession = Depends(get_db),
    ticket_in: TicketCreate,
    current_user: Any = Depends(get_current_user),
) -> Any:
    ticket_service = TicketService(db)
    return await ticket_service.create(ticket_in, str(current_user.id))


@router.get("/{ticket_id}", response_model=Ticket)
async def get_ticket(
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
    return ticket


@router.post("/{ticket_id}/messages", response_model=Message)
async def add_message(
    ticket_id: str,
    *,
    db: AsyncSession = Depends(get_db),
    message_in: MessageCreate,
    current_user: Any = Depends(get_current_user),
) -> Any:
    ticket_service = TicketService(db)
    ticket = await ticket_service.get_by_id(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if str(ticket.user_id) != str(current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return await ticket_service.add_message(ticket_id, message_in)
