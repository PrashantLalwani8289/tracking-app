from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwe, jwt
from app.common import constants
from app.config import env_variables
from sqlalchemy.orm import Session

from app.database import db_connection

security = HTTPBearer()


async def is_user_authorized(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(db_connection)
):
    try:
        token = credentials.credentials
        jwt_token = jwe.decrypt(token, "asecret128bitkey")
        
        payload = jwt.decode(jwt_token, env_variables["SECRET_KEY"], algorithms=env_variables["ALGORITHM"])
        
        id = payload.get("id")
        email = payload.get("email")
        account_type = payload.get("account_type")
        
        if not id or not email:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"error": constants.ACCESS_DENIED},
            )
            
            
        return {"id": id, "email": email, "account_type": account_type}
    
    except Exception as e:
        print(e)
        return{
            "message": constants.INVALID_TOKEN,
            "success": False,
        }
        