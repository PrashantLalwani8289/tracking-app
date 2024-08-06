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