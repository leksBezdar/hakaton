from typing import Optional

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_, update

from . import exceptions

from ..database import get_async_session
from .dao import LandmarkDAO
from .models import Landmark
from .schemas import LandmarkCreate, LandmarkBase, LandmarkUpdate


class LandmarkCrud:
    
    def __init__(self, db: AsyncSession):
        self.db = db
        
    
    async def create_landmark(self, landmark: LandmarkCreate) -> Landmark:
        
        landmark_exists = await self.get_existing_landmark(
            landmark.id, landmark.title,
            landmark.address, landmark.img)
        
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
    
    
    async def get_existing_landmark(self, id: str = None, title: str = None, address: str = None, img: str = None) -> Landmark:
        
        if not id and not str and not address and not img: 
            raise exceptions.NoCredentials
        
        landmark = await LandmarkDAO.find_one_or_none(self.db, or_(
            Landmark.id == id,
            Landmark.title == title,
            Landmark.address == address,
            Landmark.img == img,
            ))
        
        return landmark or {"message": "no landmard found"}
    
    # async def update_landmark(self, landmark: LandmarkUpdate):
        
    #     landmark = await LandmarkDAO.find_one_or_none(self.db, or_(
    #         Landmark.id == landmark.id,
    #         Landmark.title == landmark.title,
    #         Landmark.price == landmark.price,
    #         Landmark.description == landmark.description,
    #         Landmark.address == landmark.address,
    #         Landmark.time == landmark.time,
    #         Landmark.img == landmark.img,
    #         ))
              
    #     update_dict = {}

    #     fields_to_check = ['id','title', 'price', 'description', 'address', 'time', 'img']

    #     for field in fields_to_check:
    #         field_value = getattr(landmark, field, None)
    #         if field_value is not None:
    #             update_dict[getattr(Landmark, field)] = field_value
        
    #     # Меняем значение поля
    #     update_landmark = (
    #         update(Landmark)
    #         .where(or_(
    #         Landmark.id == landmark.id,
    #         Landmark.title == landmark.title,
    #         Landmark.price == landmark.price,
    #         Landmark.description == landmark.description,
    #         Landmark.address == landmark.address,
    #         Landmark.time == landmark.time,
    #         Landmark.img == landmark.img
    #         ))
    #         .values(update_dict)
    #         .returning(update_dict)
    #     )
    #     await self.db.execute(update_landmark)
        
    #     await self.db.commit()
        
    #     return {"message": "Updating successful"}
    
    
    
    async def delete_landmark(self, id: str = None, title: str = None, address: str = None) -> None:
        
        if not id and not str and not address: 
            raise exceptions.NoCredentials
        
        landmark = await self.get_existing_landmark(id=id, title=title, address=address)

        if not landmark:
            raise exceptions.LandmarkDoesNotExist
        
        await LandmarkDAO.delete(self.db, or_(
            id == landmark.id,
            title == landmark.title,
            address == landmark.address))
        
        await self.db.commit()
        
    
    
class DatabaseManager:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.landmark_crud = LandmarkCrud(db)

    # Применение изменений к базе данных
    async def commit(self):
        await self.db.commit()