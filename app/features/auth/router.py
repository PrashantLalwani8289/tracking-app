from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.schemas import ResponseModal
from app.database import db_connection
from app.features.auth.repository import (
   signup
)
from app.features.auth.schemas import (
    UserSchema,
)
from app.utils.routes import routes

router = APIRouter(prefix=routes.AUTH)



@router.post("/signup", response_model=ResponseModal)
async def signup_user(user: UserSchema, db: Session = Depends(db_connection)):
    return await signup(user, db)
