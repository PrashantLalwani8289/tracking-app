from typing import Union
from fastapi import APIRouter, Depends, Query

from app.features.adminDashboard.repository import get_mini_cards_details
from app.utils.routes import routes
from sqlalchemy.orm import Session

from app.common.schemas import ResponseModal
from app.database import db_connection

from app.utils.oauth import is_user_authorised

adminDashboardRouter = APIRouter(prefix = routes.ADMIN_DASHBOARD)


@adminDashboardRouter.get(routes.MINI_CARD_DETAILS, response_model=ResponseModal)
async def mini_cards_details(db:Session = Depends(db_connection), currentUser: dict = Depends(is_user_authorised)):
    return await get_mini_cards_details(db, currentUser)