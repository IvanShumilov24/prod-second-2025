import uuid
from typing import Optional

from app.user.models import UserModel
from app.user.service import UserService
from fastapi.params import Depends
from jose import jwt

from app.config import settings
from app.exceptions import InvalidTokenException
from app.utils import UserOAuth2PasswordBearerWithCookie

oauth2_scheme = UserOAuth2PasswordBearerWithCookie(tokenUrl="/api/user/auth/sign-in")


async def get_current_user(
        token: str = Depends(oauth2_scheme)
) -> Optional[UserModel]:
    try:
        payload = jwt.decode(token,
                             settings.RANDOM_SECRET, algorithms="HS256")
        user_id = payload.get("sub")
        if user_id is None:
            raise InvalidTokenException
    except Exception as e:
        print(e)
        raise InvalidTokenException
    current_user = await UserService.get_user(uuid.UUID(user_id))
    return current_user
