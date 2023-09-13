from typing import Optional

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_, update

from . import exceptions

from ..database import get_async_session
from .dao import LandmarkDAO, ReviewDAO
from .models import Landmark
from .schemas import LandmarkCreate, LandmarkBase


class LandmarkCrud:
    
    def __init__(self, db: AsyncSession):
        self.db = db
        
    
    async def create_landmark(self, landmark: LandmarkCreate) -> Landmark:
        
        landmark_exists = await self.get_existing_landmark(
            landmark.id, landmark.title)
        
        if landmark_exists:
            raise exceptions.LandmarkAlreadyExists
        
        db_landmark = await LandmarkDAO.add(
            self.db,
            LandmarkCreate(
            **landmark.model_dump(),
            )
        )

        self.db.add(db_landmark)
        await self.db.commit()
        await self.db.refresh(db_landmark)
        
        return db_landmark
    
    
    async def get_all_landmarks(self, *filter, offset: int = 0, limit: int = 100, **filter_by) -> list[Landmark]:
        
        landmarks = await LandmarkDAO.find_all(self.db, *filter, offset=offset, limit=limit, **filter_by)
        
        return landmarks or {"message": "no landmarks found"}
    
    
    async def get_existing_landmark(self, id: str = None, title: str = None) -> Landmark:
        
        if not id and not title: 
            raise exceptions.NoCredentials
        
        landmark = await LandmarkDAO.find_one_or_none(self.db, or_(
            Landmark.id == id,
            Landmark.title == title
            ))
        
        return landmark

    
    async def delete_landmark(self, id: str = None, title: str = None, address: str = None) -> None:
        
        if not id and not str and not address: 
            raise exceptions.NoCredentials
        
        landmark = await self.get_existing_landmark(id=id, title=title)

        if not landmark:
            raise exceptions.LandmarkDoesNotExist
        
        await LandmarkDAO.delete(self.db, or_(
            id == Landmark.id,
            title == Landmark.title,
            address == Landmark.address))
        
        await self.db.commit()


class ReviewCrud:

    def __init__(self, db: AsyncSession):
        self.db = db

    
    async def create_review(self, title: str, stars: float, description: str):

        ReviewDAO.add()


        
    
    
class DatabaseManager:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.landmark_crud = LandmarkCrud(db)

    # Применение изменений к базе данных
    async def commit(self):
        await self.db.commit()