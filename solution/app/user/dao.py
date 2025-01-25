from solution.app.dao import BaseDAO
from solution.app.user.models import UserModel
from solution.app.user.schemas import UserCreateDB, UserUpdateDB


class UserDAO(BaseDAO[UserModel, UserCreateDB, UserUpdateDB]):
    model = UserModel
