from typing import Optional
from fastapi import APIRouter, Depends, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from .dao import LandmarkDAO
from .models import Landmark
from .service import DatabaseManager
from .schemas import LandmarkCreate, LandmarkBase, LandmarkUpdate
from ..database import get_async_session


router = APIRouter()


@router.post("/create_landmark/", response_model=LandmarkBase)
async def create_landmark(
    landmark_data: LandmarkCreate,
    db: AsyncSession = Depends(get_async_session),
) -> Landmark:
    db_manager = DatabaseManager(db)
    landmark_crud = db_manager.landmark_crud
    
    return await landmark_crud.create_landmark(landmark=landmark_data)


# Получение информации о пользователе по имени пользователя
@router.get("/read_landmark", response_model=None)
async def get_landmark(
        id: str = None,
        title: str = None,
        address: str = None,
    db: AsyncSession = Depends(get_async_session),
) -> Optional[Landmark]:

    db_manager = DatabaseManager(db)
    landmark_crud = db_manager.landmark_crud
    
    landmark = await landmark_crud.get_existing_landmark(id=id, title=title)

    return landmark or {"No landmarks found"}


# Получение списка всех пользователей
@router.get("/read_all_landmarks")
async def get_all_landmarks(
    offset: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_async_session),
):
    db_manager = DatabaseManager(db)
    landmark_crud = db_manager.landmark_crud
    
    return await landmark_crud.get_all_landmarks(offset=offset, limit=limit)



@router.delete("/delete_landmark")
async def delete_landmark(
    id: str = None,
    title: str = None,
    address: str = None,
    db: AsyncSession = Depends(get_async_session),
):
    
    db_manager = DatabaseManager(db)
    landmark_crud = db_manager.landmark_crud
    
    await landmark_crud.delete_landmark(id=id, title=title, address=address)
    
    return {"message": "Deleting successful"}
