from typing import Optional
from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from .utils import OAuth2PasswordBearerWithCookie

from . import exceptions
from .models import User
from ..database import get_async_session
from .service import DatabaseManager


async def get_current_user(
        request: Request,
        token: str,
        db: AsyncSession = Depends(get_async_session),
):
    
    db_manager = DatabaseManager(db)
    user_crud = db_manager.user_crud
    token_crud = db_manager.token_crud
    
    try:
        token = token.split()[1]
        user_id = await token_crud.get_access_token_payload(token)

    except KeyError:
        raise exceptions.InvalidCredentials
    
    user = await user_crud.get_existing_user(user_id=user_id)
    return user


async def get_current_superuser(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_superuser:
        raise exceptions.NotEnoughPermissions
    return current_user


async def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_active:
        raise exceptions.InactiveUser
    return current_user
    
    
        
    
