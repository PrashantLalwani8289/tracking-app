from pydantic import BaseModel


class SubEmail(BaseModel):
    email: str
    
class ContactFormSchema(BaseModel):
    firstname: str
    lastname: str
    email: str
    subject: str
    message: str
    