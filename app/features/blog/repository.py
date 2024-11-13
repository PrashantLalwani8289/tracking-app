from datetime import datetime
from app.features.blog.schemas import CommentSchema, CreateBlog, CurrentUser, LikeSchema
from app.models.LIke import Like
from app.models.User import User
from sqlalchemy.orm import Session
from app.models.Blogs import Blogs
from app.models.Comment import Comment
from sqlalchemy import func
from sqlalchemy.orm import Session

async def create_blog(request: CreateBlog, db: Session, current_user: CurrentUser):
    try:
        print(request)
        user_id = current_user["id"]
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {
                "message": "User not found",
                "success": False,
            }

        new_blog = Blogs(
            user_id=user_id,
            destination_place= request.DestinationPlace,
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
        )
        db.add(new_blog)
        db.commit()
        db.refresh(new_blog)
        return {
            "message": "Blog created successfully",
            "success": True,
            "data": new_blog.to_dict(),
        }
    except Exception as e:
        print(e)
        return {
            "message": "An error occurred while creating the blog",
            "success": False,
        }


async def get_blog(BlogId: int, db: Session):
    try:
        blog = db.query(Blogs).filter(Blogs.id == BlogId).first()
        if not blog:
            return {
                "message": "Blog not found",
                "success": False,
            }
        return {
            "message": "Blog found successfully",
            "success": True,
            "data": blog.to_dict(),
        }
    except Exception as e:
        print(e)
        return {
            "message": "An error occurred while getting the blog",
            "success": False,
        }


async def get_all_blogs(db: Session):
    try:
        blogs = db.query(Blogs).limit(10)
        if not blogs:
            return {
                "message": "Blogs not found",
                "success": False,
            }

        return {
            "message": "Blogs found successfully",
            "success": True,
            "data": [blog.to_dict() for blog in blogs],
        }
    except Exception as e:
        print(e)
        return {
            "message": "An error occurred while getting the blog",
            "success": False,
        }


async def get_top_3_blogs(db: Session):
    try:
        blogs = (
            db.query(Blogs, func.count(Like.id).label("like_count"))
            .join(Like, Blogs.id == Like.blog_id)
            .group_by(Blogs.id)
            .order_by(func.count(Like.id).desc())
            .limit(4)
            .all()
        )
        if not blogs:
            return {
                "message": "Blogs not found",
                "success": False,
            }

        return {
            "message": "Blogs found successfully",
            "success": True,
            "data": [blog.to_dict() for blog,_ in blogs],
        }
    except Exception as e:
        print(e)
        return {
            "message": "An error occurred while getting the blog",
            "success": False,
        }


async def get_all_blogs_by_category(category: str, db: Session):
    try:
        blogs = db.query(Blogs).filter(Blogs.category == category).limit(10)
        count = db.query(Blogs).filter(Blogs.category == category).count()
        if not blogs:
            return {
                "message": "Blogs not found",
                "success": False,
            }

        return {
            "message": "Blogs found successfully",
            "success": True,
            "data": {"data": [blog.to_dict() for blog in blogs], "total_count": count},
        }
    except Exception as e:
        print(e)
        return {
            "message": "An error occurred while getting the blog",
            "success": False,
        }


async def handle_reaction(request: LikeSchema, db: Session, current_user: CurrentUser):
    try:
        current_user_id = current_user["id"]
        print(current_user)
        user = db.query(User).filter(User.id == int(current_user_id)).first()
        if not user:
            return {
                "message": "User not found",
                "success": False,
            }
        blog = db.query(Blogs).filter(Blogs.id == request.blog_id).first()
        if not blog:
            return {
                "message": "Blog not found",
                "success": False,
            }
        like = (
            db.query(Like)
            .filter(request.blog_id == Like.blog_id)
            .filter(request.user_id == Like.user_id)
            .first()
        )
        if like:
            db.delete(like)
            db.commit()
            return {
                "message": "Reaction removed successfully",
                "success": True,
            }
        like = Like(
            user_id=request.user_id,
            blog_id=request.blog_id,
        )
        db.add(like)
        db.commit()
        db.refresh(like)
        return {
            "message": "Reaction handled successfully",
            "success": True,
        }
    except Exception as e:
        print(e)
        return {
            "message": "An error occurred while handling reaction",
            "success": False,
        }


async def add_comment(request: CommentSchema, db: Session, current_user: CurrentUser):
    try:
        print(request)
        user_id = current_user["id"]
        user_email = current_user["email"]
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {
                "message": "User not found",
                "success": False,
            }

        new_comment = Comment(
            user_id=user_id,
            user_name=user_email,
            blog_id=request.blog_id,
            text=request.text,
            created_ts=datetime.now(),
            parent_id=request.parent_id if request.parent_id is not None else None,
        )
        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)
        return {
            "message": "Comment created successfully",
            "success": True,
            "data": new_comment.to_dict(),
        }
    except Exception as e:
        print(e)
        return {
            "message": "An error occurred while creating the comment",
            "success": False,
        }


async def get_all_comments(blog_id: int, comment_id: int, db: Session):
    try:
        blog = db.query(Blogs).filter(Blogs.id == blog_id).first()
        if not blog:
            return {
                "message": "Blog not found",
                "success": False,
            }
        count = 0
        if int(comment_id) != -1:
            comments = (
                db.query(Comment).filter(Comment.parent_id == comment_id).limit(10)
            )
        else:
            comments = (
                db.query(Comment)
                .filter(Comment.blog_id == blog_id)
                .filter(Comment.parent_id == None)
                .limit(10)
            )
            count = (
                db.query(Comment)
                .filter(Comment.blog_id == blog_id)
                .filter(Comment.parent_id == None)
                .count()
            )
        data = [comment.to_dict() for comment in comments]
        if len(data) == 0:
            return {"message": "No comments found", "success": True, "data": []}
        return {
            "message": "Comments fetched successfully",
            "success": True,
            "data": {"comments": data, "totalCount": count},
        }
    except Exception as e:
        print(e)
        return {
            "message": "An error occurred while fetching the comment",
            "success": False,
        }
