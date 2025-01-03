from datetime import datetime
from sqlalchemy import Index

from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    DateTime,
    Integer,
    String,
    Enum as sqEnum,
    Text,
    ARRAY,
    Float,
)
from sqlalchemy.orm import relationship
from app.database import Base


class Blogs(Base):
    __tablename__ = "blogs"
    __table_args__ = (Index("idx_user_created_ts", "user_id", "created_ts"),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    destination_place = Column(Text, default=None, nullable=True)

    title = Column(String, nullable=False)
    introduction = Column(Text, nullable=False)
    category = Column(
        sqEnum(
            "Beach",
            "Camping",
            "Hiking",
            "Desert",
            "Forest",
            "LongDrives",
            "FamilyTrips",
        ),
        nullable=False,
    )
    mainImage = Column(String, nullable=True)
    photos = Column(ARRAY(String), nullable=False)
    tips = Column(String, nullable=True)
    adventure = Column(String, nullable=False)
    accomodationReview = Column(String, nullable=True)
    destinationGuides = Column(String, nullable=True)
    customerReview = Column(String, nullable=True)
    travelChallenges = Column(String, nullable=True)
    conclusion = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
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

    comment = relationship(
        "Comment", back_populates="blog", cascade="all, delete-orphan"
    )
    # like = relationship("Like", back_populates="blog", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "introduction": self.introduction,
            "category": self.category,
            "mainImage": self.mainImage,
            "photos": self.photos,
            "tips": self.tips,
            "adventure": self.adventure,
            "accomodationReview": self.accomodationReview,
            "destinationGuides": self.destinationGuides,
            "customerReview": self.customerReview,
            "travelChallenges": self.travelChallenges,
            "conclusion": self.conclusion,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "approved": self.approved,
            "created_ts": (
                self.created_ts.isoformat() if self.created_ts else None
            ),  # Convert datetime to ISO format
            "updated_ts": (
                self.updated_ts.isoformat() if self.updated_ts else None
            ),  # Convert datetime to ISO format
        }
