from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.schemas import ResponseModal
from app.database import db_connection
from app.features.userAuth.repository import (
   google_log_in,
   login,
   signup
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
