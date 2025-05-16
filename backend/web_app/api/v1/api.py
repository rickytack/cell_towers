from fastapi import APIRouter
from .endpoints import handlers

router = APIRouter()
router.include_router(handlers.router, prefix="/v1")
