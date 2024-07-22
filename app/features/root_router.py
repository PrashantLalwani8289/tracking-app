
from fastapi import APIRouter

from .auth.router import authRouter as auth_router

router = APIRouter()

# Include all routers here
router.include_router(router=auth_router)