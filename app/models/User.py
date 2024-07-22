from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Integer, String, Enum as sqEnum, Text
from sqlalchemy.orm import relationship
from app.database import Base
# from sqlalchemy.orm import relationship



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(
        String,
    )

    email = Column(
        String,
        unique=True,
    )
    account_type = Column(
        sqEnum("user", "admin"),
        nullable=False,
    )
    password = Column(
        String,
    )
    is_active = Column(
        Boolean,
        default=False,
    )
    last_login = Column(DateTime(timezone=True), nullable=True)
    created_ts = Column(
        DateTime(timezone=True),
        default=datetime.now,
    )
    updated_ts = Column(
        DateTime(timezone=True),
        default=datetime.now,
        onupdate=datetime.now,
    )
    user_sessions = relationship("UserSession", back_populates="user")

    def to_dict(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "account_type": self.account_type,
            "created_ts": self.created_ts,
            "updated_ts": self.updated_ts,
            "last_login": self.last_login,
            "is_active": self.is_active
        }