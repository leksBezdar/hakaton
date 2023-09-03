import re
from uuid import UUID
import uuid

from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Dict, Optional


class LandmarkBase(BaseModel):
    id: str
    title: str
    rating: int
    price: int
    reviews: Dict
    description: str
    address: str
    time: str
    img: str
    
    
class LandmarkCreate(LandmarkBase):
    pass
    
    
class LandmarkUpdate(LandmarkBase):
    id: str = Field(None)
    title: str = Field(None)
    price: int = Field(None)
    description: str = Field(None)
    address: str = Field(None)
    time: str = Field(None)
    img: str = Field(None)
    