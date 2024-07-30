
from fastapi import APIRouter

from .auth.router import authRouter as auth_router
from .userAuth.router import user_router as user_router

router = APIRouter()

# Include all routers here
router.include_router(router=auth_router)
router.include_router(router=user_router)