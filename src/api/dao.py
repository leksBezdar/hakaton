from .models import Landmark
from .schemas import LandmarkCreate, LandmarkUpdate
from ..dao import BaseDAO


class LandmarkDAO(BaseDAO[Landmark, LandmarkCreate, LandmarkUpdate]):
    model = Landmark

    