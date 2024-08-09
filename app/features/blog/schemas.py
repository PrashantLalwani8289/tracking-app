from pydantic import BaseModel





class CurrentUser(BaseModel):
    id: int
    email: str
    account_type: str

class CreateBlog(BaseModel):
    title: str
    descryption:str
    mainImage:str
    category:str