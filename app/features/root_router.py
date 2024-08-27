
from fastapi import APIRouter

from .auth.router import authRouter as auth_router
from .userAuth.router import user_router as user_router
from .blog.router import blogRouter as blog_router
from .subscribers.router import subs_router as subs_router
from .adminDashboard.router import adminDashboardRouter as admin_dashboard_router
router = APIRouter()

# Include all routers here
router.include_router(router=blog_router)
router.include_router(router=auth_router)
router.include_router(router=user_router)
router.include_router(router=subs_router)
router.include_router(router=admin_dashboard_router)