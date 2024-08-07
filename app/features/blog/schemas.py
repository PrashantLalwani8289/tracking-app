from pydantic import BaseModel







class CreateBlog(BaseModel):
    title: str
    descryption:str
    mainImage:str
    category:str