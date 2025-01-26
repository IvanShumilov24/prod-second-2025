from app.user.models import UserModel
from app.user.schemas import UserCreateDB, UserUpdateDB

from app.dao import BaseDAO


class UserDAO(BaseDAO[UserModel, UserCreateDB, UserUpdateDB]):
    model = UserModel
