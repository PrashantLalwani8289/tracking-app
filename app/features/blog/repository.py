from app.features.blog.schemas import CreateBlog, CurrentUser
from app.models.User import User
from sqlalchemy.orm import Session
from app.models.Blogs import Blogs

async def create_blog(request: CreateBlog, db: Session, current_user : CurrentUser ):
    try:
        user_id = current_user["id"]
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return{
                "message": "User not found",
                "success": False,
            }
        print(request)
        print(request.mainImage)
        new_blog = Blogs(
            user_id=user_id,  
            title=request.title,
            introduction=request.introduction,
            category=request.category,
            mainImage=request.mainImage,
            photos=request.photos,
            tips=request.tips,
            adventure=request.adventure,
            accomodationReview=request.accomodationReview,
            destinationGuides=request.destinationGuides,
            customerReview=request.customerReview,
            travelChallenges=request.travelChallenges,
            conclusion=request.conclusion,
            latitude=request.latitude,
            longitude=request.longitude,
            approved=False
        )
        db.add(new_blog)
        db.commit()
        db.refresh(new_blog)  
        print(new_blog.to_dict())
        return {
            "message": "Blog created successfully",
            "success": True,
            "data": new_blog.to_dict(),
        }
    except Exception as e:
        print(e)
        return{
            "message": "An error occurred while creating the blog",
            "success": False,
        }