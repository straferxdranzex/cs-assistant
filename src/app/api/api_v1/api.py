from fastapi import APIRouter

from app.api.api_v1.endpoints import auth, tickets, ai

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(tickets.router, prefix="/tickets", tags=["tickets"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
