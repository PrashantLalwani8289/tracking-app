
from app.config import env_variables

env_data = env_variables()

from jose import jwe, jwt
from passlib.hash import bcrypt


def create_access_token(data : dict):
    to_encode = data
    # never expire OTP
    encoded_jwt = jwt.encode(
        to_encode, key=env_data["SECRET_KEY"], algorithm=env_data["ALGORITHM"]
    )
    encoded_jwe = jwe.encrypt(
        encoded_jwt,
        "asecret128bitkey",
        algorithm="dir",
        encryption="A128GCM",
    )
    return encoded_jwe
    