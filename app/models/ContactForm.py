from app.database import Base
from sqlalchemy import  Column,  Integer, String

class ContactForm(Base):
    __tablename__ = 'contact_form'
    id = Column(Integer, primary_key=True)
    
    full_name = Column(
        String,
        nullable=False
    )
    
    email = Column(
        String,
        nullable=False
    )
    
    subject = Column(String, nullable=True)
    message = Column(String, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'subject': self.subject,
            'message': self.message
        }