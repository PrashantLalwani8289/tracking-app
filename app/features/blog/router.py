

from fastapi import APIRouter, Depends
from app.features.blog.repository import create_blog
from app.features.blog.schemas import CreateBlog
from app.utils.routes import routes
from sqlalchemy.orm import Session

from app.common.schemas import ResponseModal
from app.database import db_connection

blogRouter = APIRouter(prefix = routes.BLOG)


@blogRouter.post(routes.CREATE_BLOG, response_model=ResponseModal)
async def create_new_blog(request: CreateBlog, db: Session = Depends(db_connection)):
    return await create_blog(request, db) 