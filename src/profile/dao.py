from auth.models import User
from auth.schemas import UserCreateDB, UserUpdate
from ..dao import BaseDAO
from .models import FavoriteList


class UserDAO(BaseDAO[User, UserCreateDB, UserUpdate]):
    model = User