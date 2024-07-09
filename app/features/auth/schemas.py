from pydantic import BaseModel

from pydantic.networks import EmailStr

class UserSchema(BaseModel):
    full_name: str
    email: EmailStr
    password: str
