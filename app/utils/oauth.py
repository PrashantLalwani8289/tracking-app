from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwe, jwt
from sqlalchemy.orm import Session

from app.common import constants
from app.config import env_variables
from app.database import db_connection

# from app.features.aws.secretKey import get_secret_keys
from app.models.User import User
from app.models.user_sessions import UserSession

env_data = env_variables()


security = HTTPBearer()


async def is_user_authorised(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(db_connection),
) -> dict:
    try:
        token = credentials.credentials
        jwt_token = jwe.decrypt(token, "asecret128bitkey")

        payload = jwt.decode(
            jwt_token, env_data["SECRET_KEY"], algorithms=env_data["ALGORITHM"]
        )

        id = payload.get("id")
        email = payload.get("email")
        account_type = payload.get("account_type")
        print(payload)
        if not id or not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"error": constants.ACCESS_DENIED},
            )

        user = db.query(User).get(id)
        user_session = (
            db.query(UserSession)
            .filter(UserSession.user_id == id, UserSession.token == token)
            .first()
        )

        if user_session is None:
            raise ValueError(constants.TOKEN_NOT_FOUND)

        if not user:
            raise ValueError(constants.USER_NOT_FOUND)
        return {"id": id, "email": email, "account_type": account_type}
    except Exception as e:
        print(e, "Exception")
        error_message = str(e)
        if error_message == constants.USER_INACTIVE:
            detail = constants.USER_INACTIVE
        else:
            detail = constants.INVALID_TOKEN
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": detail},
        )
