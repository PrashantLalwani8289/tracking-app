# CSRF Token Generation:

# Use the /csrf-token route to fetch a CSRF token. The frontend should store this token (e.g., in a meta tag or JavaScript variable).
# CSRF Token Validation:

# In protected routes (e.g., /protected-route), the token must be included in the request's body, header, or form data.
# The backend validates the token using csrf_protect.validate_csrf().
# Token Storage:

# The token can be sent in headers or form data by the frontend, ensuring it is not exposed in cookies or URLs.
import threading
from app.utils.Jobs.jobs import BackgroundTasks
from confluent_kafka import Producer, Consumer, KafkaException
from datetime import datetime
import json
from fastapi_csrf_protect import CsrfProtect
from sqlalchemy import desc
from app.features.blog.response import GPT
from app.features.blog.schemas import (
    CommentSchema,
    CreateBlog,
    CurrentUser,
    Destination,
    GetLikes,
    LikeSchema,
)
from app.models import Subscribers
from app.models.LIke import Like
from app.models.User import User
from sqlalchemy.orm import Session
from app.models.Blogs import Blogs
from app.models.Comment import Comment
from sqlalchemy import func
from sqlalchemy.orm import Session

kafka_bootstrap_servers = "localhost:9092"
topic = "likes_topic"

from app.utils.Jobs.background import jobs

producer = Producer({"bootstrap.servers": kafka_bootstrap_servers})


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
            destination_place=request.DestinationPlace,
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


async def get_all_blogs(db: Session, csrf_protect: CsrfProtect):

    try:
        # csrf_protect
        # csrf_protect.validate_csrf_in_cookies()
        token = csrf_protect.generate_csrf()
        print(token, "token")
        print(csrf_protect)
        blogs = (
            db.query(Blogs)
            # .filter(Blogs.user_id == user_id)
            .order_by(desc(Blogs.created_ts)).all()
        )
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
            "data": [blog.to_dict() for blog, _ in blogs],
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
        print(request, "request")
        print(current_user, "current_user")
        producer.produce(topic, key="like", value="1")
        producer.flush()
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
            .filter(current_user_id == Like.user_id)
            .all()
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
        print("like: ", like.to_dict())
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


# threading.Thread(target=jobs.consume_likes, daemon=True).start()

# def consume_likes():
#     consumer = Consumer(
#         {
#             "bootstrap.servers": kafka_bootstrap_servers,
#             "group.id": "like-counter-group",
#             "auto.offset.reset": "earliest",
#         }
#     )
#     consumer.subscribe([topic])

#     try:
#         while True:
#             msg = consumer.poll(1.0)
#             if msg is None:
#                 continue
#             if msg.error():
#                 if msg.error().code() == KafkaException._PARTITION_EOF:
#                     continue
#                 else:
#                     print(msg.error())
#                     break
#             # Update like count
#             likes_count["total_likes"] += 1
#             print(f"Total likes: {likes_count['total_likes']}")
#     finally:
#         consumer.close()


def get_likes():
    # print(current_user)
    likes = jobs.likes_count_value
    print(likes, "from socket")
    return likes


async def get_is_liked(request: GetLikes, db: Session, current_user: CurrentUser):
    try:
        user_id = current_user["id"]
        print(user_id, request.blog_id)
        like = (
            db.query(Like)
            .filter(request.blog_id == Like.blog_id)
            .filter(Like.user_id == int(user_id))
            .first()
        )
        print(like, "like")
        if like:
            return {
                "message": "User has liked the blog",
                "success": True,
            }
        return {
            "message": "User has not liked the blog",
            "success": True,
        }
    except Exception as e:
        print(e)


# Start Kafka consumer in a separate thread


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


async def get_destination_summary(
    request: Destination, db: Session, current_user: CurrentUser
):
    try:
        user_id = current_user["id"]
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return {
                "message": "User not found",
                "success": False,
            }
        destination = request.destination
        response = GPT().query(input=destination)
        # data = json.loads(response)
        return {
            "message": "Destination summary fetched successfully",
            "success": True,
            "data": response,
        }
    except Exception as e:
        print(e)
        return {
            "message": "An error occurred while fetching the destination summary",
            "success": False,
        }


async def get_about_page_details(db: Session):
    try:
        total_blogs = db.query(Blogs).count()
        total_subscribers = db.query(Subscribers).count()

        return {
            "message": "About page details fetched successfully",
            "success": True,
            "data": [],
        }
    except Exception as e:
        print(e)
        return {
            "message": "An error occurred while fetching about page details",
            "success": False,
        }
