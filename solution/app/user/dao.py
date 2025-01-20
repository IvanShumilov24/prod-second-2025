from solution.app.user.models import UserModel
from solution.app.user.schemas import UserCreateDB


class UserDAO(BaseDAO[UserModel, UserCreateDB, UserUpdateDB]):
    model = UserModel
