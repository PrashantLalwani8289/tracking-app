

from typing import Union
from fastapi import APIRouter, Depends, Query
from app.features.blog.repository import add_comment, create_blog, get_all_blogs, get_blog, handle_reaction
from app.features.blog.schemas import  CommentSchema, CreateBlog
from app.utils.routes import routes
from sqlalchemy.orm import Session

from app.common.schemas import ResponseModal
from app.database import db_connection

from app.utils.oauth import is_user_authorised

blogRouter = APIRouter(prefix = routes.BLOG)


@blogRouter.post(routes.CREATE_BLOG, response_model=ResponseModal)
async def create_new_blog(request: CreateBlog, db: Session = Depends(db_connection), currentUser: dict = Depends(is_user_authorised)):
    return await create_blog(request, db, currentUser) 

@blogRouter.get(routes.GET_BLOG, response_model=ResponseModal)
async def get_the_blog(BlogId: Union[int, str] = Query(-1,description="Enter the blog id"), db: Session = Depends(db_connection)):
    return await get_blog(BlogId, db) 


@blogRouter.get(routes.GET_ALL_BLOG, response_model=ResponseModal)
async def get_the_blog( db: Session = Depends(db_connection)):
    return await get_all_blogs(db) 

@blogRouter.get(routes.HANDLE_REACTION, response_model=ResponseModal)
async def handle_like( db: Session = Depends(db_connection)):
    return await handle_reaction(db) 

@blogRouter.post(routes.ADD_COMMENT, response_model=ResponseModal)
async def add_new_comment(request: CommentSchema, db: Session = Depends(db_connection), currentUser: dict = Depends(is_user_authorised)):
    return await add_comment(request, db, currentUser)