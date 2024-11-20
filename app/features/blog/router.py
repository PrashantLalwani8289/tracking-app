from typing import Union
from fastapi import APIRouter, Depends, Query
from app.features.blog.repository import (
    add_comment,
    create_blog,
    get_all_blogs,
    get_all_blogs_by_category,
    get_all_comments,
    get_blog,
    get_destination_summary,
    get_top_3_blogs,
    handle_reaction,
)
from app.features.blog.schemas import CommentSchema, CreateBlog, Destination, LikeSchema
from app.utils.routes import routes
from sqlalchemy.orm import Session

from app.common.schemas import ResponseModal
from app.database import db_connection

from app.utils.oauth import is_user_authorised

blogRouter = APIRouter(prefix=routes.BLOG)


@blogRouter.post(routes.CREATE_BLOG, response_model=ResponseModal)
async def create_new_blog(
    request: CreateBlog,
    db: Session = Depends(db_connection),
    currentUser: dict = Depends(is_user_authorised),
):
    return await create_blog(request, db, currentUser)


@blogRouter.get(routes.GET_BLOG, response_model=ResponseModal)
async def get_the_blog(
    BlogId: Union[int, str] = Query(-1, description="Enter the blog id"),
    db: Session = Depends(db_connection),
):
    return await get_blog(BlogId, db)


@blogRouter.get(routes.GET_ALL_BLOG, response_model=ResponseModal)
async def get_the_blog(db: Session = Depends(db_connection)):
    return await get_all_blogs(db)


@blogRouter.get(routes.GET_TOP_3_BLOGS, response_model=ResponseModal)
async def get_the_blog(db: Session = Depends(db_connection)):
    return await get_top_3_blogs(db)


@blogRouter.get(routes.GET_ALL_BLOG_BY_CATEGORY, response_model=ResponseModal)
async def get_the_blog(
    category: str = Query("all"), db: Session = Depends(db_connection)
):
    return await get_all_blogs_by_category(category, db)


@blogRouter.post(routes.HANDLE_REACTION, response_model=ResponseModal)
async def handle_like(
    request: LikeSchema,
    db: Session = Depends(db_connection),
    currentUser: dict = Depends(is_user_authorised),
):
    return await handle_reaction(request, db, currentUser)


@blogRouter.post(routes.ADD_COMMENT, response_model=ResponseModal)
async def add_new_comment(
    request: CommentSchema,
    db: Session = Depends(db_connection),
    currentUser: dict = Depends(is_user_authorised),
):
    return await add_comment(request, db, currentUser)


@blogRouter.get(routes.GET_COMMENTS, response_model=ResponseModal)
async def get_comments(
    blog_id: Union[int, str] = Query(-1),
    comment_id: Union[int, str] = Query(-1),
    db: Session = Depends(db_connection),
):
    return await get_all_comments(blog_id, comment_id, db)


@blogRouter.post(routes.GET_AUTO_BLOGS, response_model=ResponseModal)
async def get_comments(
    request: Destination,
    db: Session = Depends(db_connection),
    currentUser: dict = Depends(is_user_authorised),
):
    return await get_destination_summary(request, db, currentUser)
