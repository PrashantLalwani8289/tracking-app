
from app.features.blog.schemas import CurrentUser
from app.models.User import User
from sqlalchemy.orm import Session
from app.models.Blogs import Blogs

async def get_mini_cards_details(db : Session, current_user : CurrentUser):
    try:
        user_id = current_user["id"]
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return{
                "message": "User not found",
                "success": False,
            }
        if(user.account_type != "admin"):
            return{
                "message": "Unauthorized",
                "success": False,
            }
            
            
        blogs = db.query(Blogs).count()
        verified_blogs = db.query(Blogs).filter(Blogs.approved  == True).count()
        unverified_blogs = db.query(Blogs).filter(Blogs.approved  == False).count()
        
        users = db.query(User).filter(User.account_type != "admin").count()
        active_users = db.query(User).filter(User.is_active == True).filter(User.account_type != "admin").count()
        inactive_users = db.query(User).filter(User.is_active == False).filter(User.account_type != "admin").count()
        return{
            "message": "Mini cards fetched successfully",
            "success": True,
            "data": {
                "total_blogs": blogs,
                "verified_blogs": verified_blogs,
                "unverified_blogs": unverified_blogs,
                "total_users": users,
                "active_users": active_users,
                "inactive_users": inactive_users,
            }
        }
    except Exception as e:
        print(e)
        return{
            "message": "An error occurred while getting mini cards",
            "success": False,
        }