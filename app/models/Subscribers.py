
from app.database import Base
from sqlalchemy import  Column,  Integer, String



class Subscribers(Base):
    __tablename__ = 'subscribers'
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    
    
    def to_dict(self):
        return{
            'id': self.id,
            'email': self.email
        }