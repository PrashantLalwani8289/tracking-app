
from fastapi import APIRouter

from .auth.router import router as auth_router

router = APIRouter()

# Include all routers here
router.include_router(router=auth_router)