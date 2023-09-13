import uuid
import jwt

from typing import Optional
from uuid import uuid4

from datetime import datetime, timedelta, timezone

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_, update

from . import schemas, models, exceptions

from ..database import get_async_session
from auth.config import(
    TOKEN_SECRET_KEY,
    ALGORITHM,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS
    )
from .dao import UserDAO
from .models import FavoriteList
from auth.schemas import UserUpdate
from auth.service import DatabaseManager


# Определение класса для управления операциями с пользователями в базе данных
class UserCRUD:
    
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_current_user(self, token: str):

        db_manager = DatabaseManager(db)
        token_crud = db_manager.token_crud

        try:
        user_id = await token_crud.get_access_token_payload(token)

    except KeyError:
        raise exceptions.InvalidCredentials
    
    user = await user_crud.get_existing_user(user_id=user_id)
    return user

    async def get_user_favorite_list(self, user: User):

        



