from fastapi import APIRouter, Depends
from app.features.subscribers.repository import (
    contact_form,
    count_subs,
    sub_for_newsletter,
)
from sqlalchemy.orm import Session

from app.common.schemas import ResponseModal
from app.database import db_connection
from app.features.subscribers.schemas import ContactFormSchema, SubEmail


from app.utils.routes import routes

subs_router = APIRouter(prefix=routes.SUBSCRIBE)


@subs_router.post(routes.SUBSCRIBE_NEW_USER, response_model=ResponseModal)
async def subscribe(request: SubEmail, db: Session = Depends(db_connection)):
    return await sub_for_newsletter(request, db)


@subs_router.post(routes.CONTACT_FORM, response_model=ResponseModal)
async def ContactUs(request: ContactFormSchema, db: Session = Depends(db_connection)):
    return await contact_form(request, db)


@subs_router.get(routes.SUB_COUNT, response_model=ResponseModal)
async def getSubCount(db: Session = Depends(db_connection)):
    return await count_subs(db)
