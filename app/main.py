from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import settings
from .features.root_router import router as root_router


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "*"
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _app.include_router(router=root_router, prefix=settings.API_V1_STR)

    return _app


app = get_application()
