from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

# from app.utils.Jobs.jobs import BackgroundTasks
from app.utils.Jobs.background import jobs
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from pydantic import BaseModel

# from fastapi.routing import APIRouter


from .core.config import settings
from .features.root_router import router as root_router


jobs.start()


def get_application():
    limiter = Limiter(key_func=get_remote_address)
    _app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    _app.state.limiter = limiter
    _app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            # "http://localhost:5173",
            # "http://localhost:5174",
            # "ws://localhost:5173",
            # "ws://localhost:5174",
            "*",
        ],
        allow_credentials=True,
        allow_methods=["GET", "POST", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type"],
    )
    # _app.add_middleware(HTTPSRedirectMiddleware)

    _app.include_router(router=root_router, prefix=settings.API_V1_STR)

    return _app


app = get_application()
