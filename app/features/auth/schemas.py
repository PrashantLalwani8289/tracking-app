from pydantic import BaseModel, EmailStr

class UserSchema(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    confirm_password : str
    


class LoginUserSchema(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    credentials: str

