from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.schemas import ResponseModal
from app.database import db_connection
from app.features.auth.repository import (
   login,
   signup
)
from app.features.auth.schemas import (
    UserSchema,
    LoginUserSchema
)
from app.utils.routes import routes

router = APIRouter(prefix=routes.AUTH)



@router.post(routes.SIGNUP, response_model=ResponseModal)
async def signup_user(request: UserSchema, db: Session = Depends(db_connection)):
    return await signup(request, db)



@router.post(routes.LOGIN, response_model=ResponseModal)
async def login_user(request: LoginUserSchema, db: Session = Depends(db_connection)):
    return await login(request, db)
