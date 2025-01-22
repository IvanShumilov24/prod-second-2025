import uuid

from fastapi.params import Depends
from jose import jwt
from typing_extensions import Optional

from solution.app.business.models import BusinessModel
from solution.app.business.service import BusinessService
from solution.app.business.utils import OAuth2PasswordBearerWithCookie
from solution.app.config import settings
from solution.app.exceptions import InvalidTokenException

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/api/auth/login")


async def get_current_business(
        token: str = Depends(oauth2_scheme)
) -> Optional[BusinessModel]:
    try:
        payload = jwt.decode(token,
                             settings.RANDOM_SECRET, algorithms='HS256')
        business_id = payload.get("sub")
        if business_id is None:
            raise InvalidTokenException
    except Exception as e:
        print(e)
        raise InvalidTokenException
    current_business = await BusinessService.get_business(uuid.UUID(business_id))
    return current_business
