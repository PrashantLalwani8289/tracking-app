import json
import os
from datetime import datetime

from passlib.hash import bcrypt
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.common import constants
from app.config import env_variables
from app.features.auth.schemas import (
    UserSchema
)

from app.models.User import User

env_data = env_variables()


async def signup(request: UserSchema, db : Session):
    try:
        password_hash = bcrypt.hash(request.password)
        
        existing_user = (
            db.query(User).filter(User.email == request.email.lower()).first()
        )

        if existing_user:
            return {
                "message": constants.USER_WITH_EMAIL_ALREADY_EXISTS,
                "success": False,
            }
        else:
            # Create a new user object
            new_user = User(
                full_name=request.full_name,
                email=request.email.lower(),
                password=password_hash,
                account_type="user",
            )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return {
            "message": constants.SIGNUP_SUCCESS,
            "success": True,
            "data": UserSchema().dump(new_user),
        }
    except Exception as e:
        print("error in signup", e)
        return {
            "message": constants.INTERNAL_SERVER_ERROR,
            "success": False,
        }