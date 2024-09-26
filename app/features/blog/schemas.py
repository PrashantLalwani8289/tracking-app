
from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional
from enum import Enum


class CurrentUser(BaseModel):
    id: int
    email: str
    account_type: str

class CategoryEnum(str, Enum):
    Camping="Camping"
    Hiking="Hiking"
    Desert="Desert"
    Forest="Forest"
    LongDrives="LongDrives"
    FamilyTrips="FamilyTrips"
    Beach="Beach"
    
    
class CreateBlog(BaseModel):
    title: str = Field(..., example="My Travel Adventure")
    category: CategoryEnum = Field(..., example="Travel")
    mainImage: Optional[str] = Field(None, example="https://example.com/image.jpg")
    introduction: str = Field(..., example="This blog post is about...")
    photos: List[str] = Field(..., example=["https://example.com/photo1.jpg", "https://example.com/photo2.jpg"])
    tips: Optional[str] = Field(None, example="Pack light, always carry a first-aid kit.")
    adventure: str = Field(..., example="Hiking in the Alps")
    accomodationReview: Optional[str] = Field(None, example="Stayed at a cozy mountain lodge...")
    destinationGuides: Optional[str] = Field(None, example="Top 10 things to do in Paris...")
    customerReview: Optional[str] = Field(None, example="The service was excellent!")
    travelChallenges: Optional[str] = Field(None, example="Lost luggage at the airport...")
    conclusion: str = Field(..., example="Overall, it was a fantastic trip.")
    latitude: float = Field(..., example=48.858844)
    longitude: float = Field(..., example=2.294351)    
    
    
class LikeSchema(BaseModel):
    blog_id : int
    user_id: int
class CommentSchema(BaseModel):
    user_id : int | None = None
    blog_id : int
    text : str
    parent_id: int | None = None

