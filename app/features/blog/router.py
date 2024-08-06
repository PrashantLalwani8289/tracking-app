

from fastapi import APIRouter, Depends
from app.utils import routes
from sqlalchemy.orm import Session

from app.common.schemas import ResponseModal
from app.database import db_connection

blogRouter = APIRouter(prefix = routes.BLOG)


@blogRouter.post(routes.CREATE_BLOG, response_model=ResponseModal)
async def signup_user(request: UserSchema, db: Session = Depends(db_connection)):
    return await signup(request, db)