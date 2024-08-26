from typing import Union
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.common.schemas import ResponseModal
from app.database import db_connection
from app.features.userAuth.repository import (
   get_user,
   get_user_blogs,
   google_log_in,
   login,
   signup,
   upload_blog_image
)
from app.features.userAuth.schemas import (
    Token, 
    UserSchema,
    LoginUserSchema
)
from app.utils.routes import routes

user_router = APIRouter(prefix=routes.USER)



@user_router.post(routes.SIGNUP, response_model=ResponseModal)
async def signup_user(request: UserSchema, db: Session = Depends(db_connection)):
    return await signup(request, db)



@user_router.post(routes.LOGIN, response_model=ResponseModal)
async def login_user(request: LoginUserSchema, db: Session = Depends(db_connection)):
    return await login(request, db)


@user_router.post(routes.GOOGLE_SIGN_IN, response_model=ResponseModal)
async def signin_with_google(request:Token, db: Session = Depends(db_connection)):
    return await google_log_in(request, db)

@user_router.get(routes.UPLOAD_BLOG_IMAGE, response_model=ResponseModal)
async def upload_image():
    return await upload_blog_image()

@user_router.get(routes.GET_USER, response_model=ResponseModal)
async def get_user_details(userId : Union[int, str] =  Query(-1, description="Getting user id for user details"), db : Session = Depends(db_connection)):
    return await get_user(userId, db)

@user_router.get(routes.GET_USER_BLOGS, response_model=ResponseModal)
async def get_user_blogs_details(userId : Union[int, str] =  Query(-1, description="Getting user id for user details"), db : Session = Depends(db_connection)):
    return await get_user_blogs(userId, db)
