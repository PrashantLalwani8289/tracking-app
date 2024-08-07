from datetime import datetime

from sqlalchemy import Boolean, Column, ForeignKey, DateTime, Integer, String, Enum as sqEnum, Text
from sqlalchemy.orm import relationship
from app.database import Base





class Blogs(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(
        String,
        nullable=False
    )
    descryption = Column(
        Text,
        nullable=False
    )
    category =  Column(
        sqEnum("Technology", "Health", "Travel", "Education", "Finance"),
        nullable=False,
    )
    mainImage = Column(
        String,
        nullable=True
    )
    approved = Column(
        Boolean,
        default=False,
        nullable=False,
    )
    created_ts = Column(
        DateTime(timezone=True),
        default=datetime.now,
    )
    updated_ts = Column(
        DateTime(timezone=True),
        default=datetime.now,
        onupdate=datetime.now,
    )
    
    user = relationship(
        "User",
        back_populates="blogs",
        cascade="all, delete-orphan",
        single_parent=True,
    )
    
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "descryption": self.descryption,
            "category": self.category,
            "mainImage": self.mainImage,
            "approved": self.approved,
            "created_ts": self.created_ts.isoformat() if self.created_ts else None,
            "updated_ts": self.updated_ts.isoformat() if self.updated_ts else None,
        }