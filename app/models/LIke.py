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