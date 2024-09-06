from datetime import datetime

from sqlalchemy import ForeignKey, Column, DateTime, Integer,  Text
from sqlalchemy.orm import relationship
from app.database import Base



class Comment(Base):
    __tablename__ = "comment"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    blog_id = Column(Integer, ForeignKey('blogs.id')) 
    text = Column(Text, nullable=False)
    created_ts = Column(
        DateTime(timezone=True),
        default=datetime.now,
    )
    updated_ts = Column(
        DateTime(timezone=True),
        default=datetime.now,
        onupdate=datetime.now,
    )
    parent_id = Column(Integer, default=None);
    
    user = relationship(
        "User",
        back_populates="comment",
        cascade="all, delete-orphan",
        single_parent=True,
    )
    
    blog = relationship("Blogs", back_populates="comment", cascade="all, delete-orphan", single_parent=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "blog_id": self.blog_id,
            "text": self.text,
            "created_ts": self.created_ts,
            "updated_ts": self.updated_ts,
            "parent_id": self.parent_id if self.parent_id is not None else None
        }
    
    