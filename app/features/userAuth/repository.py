import json
import os
from datetime import datetime
from pydantic.networks import EmailStr
import hmac
import hashlib
import base64
import time
from sqlalchemy import desc
from passlib.hash import bcrypt
from app.features.userAuth.utils import create_access_token, generate_random_password
from app.models.Blogs import Blogs
from sqlalchemy import and_
from sqlalchemy.orm import Session
from google.oauth2 import id_token
from google.auth.transport import requests

from app.common import constants
from app.config import env_variables
from app.features.userAuth.schemas import (
    LoginUserSchema,
    Token,
    UploadImage,
    UserSchema,
)

from app.models.User import User
from app.models.user_sessions import UserSession

env_data = env_variables()

GOOGLE_CLIENT_ID = env_data["GOOGLE_CLIENT_ID"]


async def signup(request: UserSchema, db: Session):
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
        if request.password != request.confirm_password:
            return {
                "message": "Passwords do not match",
                "success": False,
            }
            # Create a new user object
        new_user = User(
            full_name=request.full_name,
            email=request.email.lower(),
            password=password_hash,
            account_type="user",
            is_active=True,
            last_login=datetime.now(),
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        payload = {"id": new_user.id, "email": new_user.email, "account_type": "user"}
        access_token = create_access_token(payload)
        session = UserSession(user_id=new_user.id, token=access_token.decode())
        db.add(session)
        db.commit()

        return {
            "message": constants.SIGNUP_SUCCESS,
            "success": True,
            "data": {
                "user": {
                    "token": access_token,
                    "name": new_user.full_name,
                    "email": new_user.email,
                    "id": new_user.id,
                },
            },
        }
    except Exception as e:
        print("error in signup", e)
        return {
            "message": constants.INTERNAL_SERVER_ERROR,
            "success": False,
        }


async def login(request: LoginUserSchema, db: Session):
    try:
        existing_user = (
            db.query(User).filter(User.email == request.email.lower()).first()
        )
        if not existing_user:
            return {
                "message": constants.USER_NOT_FOUND,
                "success": False,
            }
        if existing_user and bcrypt.verify(request.password, existing_user.password):
            existing_user.last_login = datetime.now()
            payload = {
                "id": existing_user.id,
                "email": existing_user.email,
                "account_type": "user",
            }
            access_token = create_access_token(payload)
            session = UserSession(user_id=existing_user.id, token=access_token.decode())
            db.add(session)
            db.commit()

            return {
                "message": constants.LOGIN_SUCCESS,
                "success": True,
                "data": {
                    "user": {
                        "token": access_token,
                        "name": existing_user.full_name,
                        "email": existing_user.email,
                        "id": existing_user.id,
                    },
                },
            }

        else:
            return {
                "message": constants.INCORRECT_CREDENTIALS,
                "success": False,
            }

    except Exception as e:
        print("error in login", e)
        return {
            "message": constants.INTERNAL_SERVER_ERROR,
            "success": False,
        }


async def google_log_in(request: Token, db: Session):
    try:
        id_info = id_token.verify_oauth2_token(
            request.credentials, requests.Request(), GOOGLE_CLIENT_ID
        )
        if id_info["iss"] not in ["accounts.google.com", "https://accounts.google.com"]:
            return {
                "message": constants.INVALID_GOOGLE_TOKEN,
                "success": False,
            }
        email = id_info.get("email")
        full_name = id_info.get("name")
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            existing_user.last_login = datetime.now()
            db.commit()
            payload = {
                "id": existing_user.id,
                "email": existing_user.email,
                "account_type": "user",
            }
            access_token = create_access_token(payload)
            session = UserSession(user_id=existing_user.id, token=access_token.decode())
            db.add(session)
            db.commit()

            return {
                "message": constants.LOGIN_SUCCESS,
                "success": True,
                "data": {
                    "user": {
                        "token": access_token,
                        "name": existing_user.full_name,
                        "email": existing_user.email,
                        "id": existing_user.id,
                    },
                },
            }
        else:
            password = generate_random_password()
            password_hash = bcrypt.hash(password)
            new_user = User(
                full_name=full_name,
                email=email,
                password=password_hash,
                account_type="user",
                is_active=True,
                last_login=datetime.now(),
            )
            payload = {
                "id": existing_user.id,
                "email": existing_user.email,
                "account_type": "user",
            }
            access_token = create_access_token(payload)
            session = UserSession(user_id=new_user.id, token=access_token.decode())
            db.add(session)
            db.commit()
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return {
                "message": constants.LOGIN_SUCCESS,
                "success": True,
                "data": {
                    "user": {
                        "token": access_token,
                        "name": new_user.full_name,
                        "email": new_user.email,
                        "id": new_user.id,
                    },
                },
            }

    except Exception as e:
        print(e)
        return {
            "message": constants.INTERNAL_SERVER_ERROR,
            "success": False,
        }


IMAGEKIT_PRIVATE_KEY = env_data["IMAGEKIT_PRIVATE_KEY"]


# IMAGEKIT_PUBLIC_KEY = env_data['IMAGEKIT_PUBLIC_KEY']
# IMAGEKIT_URL_ENDPOINT = env_data['IMAGEKIT_URL_ENDPOINT']
async def upload_blog_image():
    try:
        token = base64.urlsafe_b64encode(os.urandom(32)).decode()
        expire = str(int(time.time()) + 600)  # Token is valid for 10 minutes
        signature = hmac.new(
            IMAGEKIT_PRIVATE_KEY.encode(), (token + expire).encode(), hashlib.sha1
        ).hexdigest()
        return {
            "message": constants.UPLOAD_BLOG_IMAGE_SUCCESSFULL,
            "success": True,
            "data": {"token": token, "expire": expire, "signature": signature},
        }
    except Exception as e:
        print(e)
        return {
            "message": constants.INTERNAL_SERVER_ERROR,
            "success": False,
        }


async def get_user(userId: int, db=Session):
    try:
        user = db.query(User).filter(User.id == userId).first()
        if user:
            return {
                "message": constants.USER_FOUND,
                "success": True,
                "data": {
                    "user": {
                        "id": user.id,
                        "name": user.full_name,
                        "email": user.email,
                        "account_type": user.account_type,
                        "is_active": user.is_active,
                        "last_login": user.last_login,
                    }
                },
            }
        else:
            return {
                "message": constants.USER_NOT_FOUND,
                "success": False,
            }
    except Exception as e:
        print("error in getUser", e)
        return {
            "message": constants.INTERNAL_SERVER_ERROR,
            "success": False,
        }


async def get_user_blogs(userId: int, db=Session):
    try:
        user = db.query(User).filter(User.id == userId).first()
        if not user:
            return {
                "message": constants.USER_NOT_FOUND,
                "success": False,
            }
        blogs = (
            db.query(Blogs)
            .filter(Blogs.user_id == userId)
            .order_by(desc(Blogs.created_ts))
            .all()
        )
        if blogs:
            return {
                "message": constants.BLOGS_FOUND,
                "success": True,
                "data": [blog.to_dict() for blog in blogs],
            }
        else:
            return {
                "message": constants.BLOGS_NOT_FOUND,
                "success": False,
                "data": [],
            }
    except Exception as e:
        print("error in getUser", e)
        return {
            "message": constants.INTERNAL_SERVER_ERROR,
            "success": False,
        }
