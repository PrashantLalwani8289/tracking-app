from pydantic import BaseModel, EmailStr

class UserSchema(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: str


