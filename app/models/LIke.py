from datetime import datetime
from sqlalchemy import ForeignKey, Column, DateTime, Integer
from sqlalchemy.orm import relationship
from app.database import Base


class Like(Base):
    __tablename__ = "like"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    blog_id = Column(Integer, nullable=False)
    created_ts = Column(DateTime, default=datetime.now)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "blog_id": self.blog_id,
            "created_ts": self.created_ts.isoformat() if self.created_ts else None,
        }
