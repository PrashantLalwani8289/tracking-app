

from app.features.subscribers.schemas import ContactFormSchema, SubEmail
from app.models.ContactForm import ContactForm
from app.models.Subscribers import Subscribers
from app.models.User import User
from sqlalchemy.orm import Session
async def sub_for_newsletter(request: SubEmail, db: Session):
    try:
        existing_subscriber = db.query(Subscribers).filter(request.email == Subscribers.email).first()
        if existing_subscriber:
            return{
                "message": "Email already subscribed",
                "success": False,
            }
        # existing_user = db.query(User).filter(request.email == User.email).first()
        # if existing_user:
        #     return{
        #         "message": "This user is already subscribed",
        #         "success": False,
        #     }
        new_subscriber = Subscribers(
            email=request.email
        )
        db.add(new_subscriber)
        db.commit()
        db.refresh(new_subscriber)
        return{
            "message": "Email subscribed successfully",
            "success": True,
            "data": new_subscriber.to_dict(),
        }
    except Exception as e:
        print(e)
        return{
            "message": "An error occurred while subscribing for newsletter",
            "success": False,
        }
        
        
async def contact_form(request : ContactFormSchema , db : Session):
    try:
        new_contact = ContactForm(
            full_name=str(request.firstname + " " + request.lastname),
            email=request.email,
            subject=request.subject,
            message=request.message
        )
        db.add(new_contact)
        db.commit()
        db.refresh(new_contact)
        return{
            "message": "Form submitted successfully",
            "success": True,
            "data": new_contact.to_dict(),
        }
    except Exception as e:
        print(e)
        return{
            "message": "An error occurred while submitting the contact form",
            "success": False,
        }