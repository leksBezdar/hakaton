from fastapi import APIRouter, Depends, Request, Response
from auth.dependencies import get_current_user
from request import Request
from auth.models import User
from .dao import *

router = APIRouter()

@router.get("/me")
async def get_current_user(db: AsyncSession = Depends(get_async_session), request: Request):

    access_token = request.cookies.get('access_token')

    return get_current_user(request=request, token=access_token)

@router.get("/favorite_landmarks")
async def get_favorite_landmarks(
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
    ):

    return current_user.favorite_landmarks

@router.get("/published_landmarks")
async def get_published_landmarks(
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_user),
    ):

    return current_user.published_landmarks


