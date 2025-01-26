import uuid

from app.business.models import BusinessModel
from app.business.service import BusinessService
from fastapi.params import Depends
from jose import jwt
from typing_extensions import Optional

from app.config import settings
from app.exceptions import InvalidTokenException
from app.utils import BusinessOAuth2PasswordBearerWithCookie

oauth2_scheme = BusinessOAuth2PasswordBearerWithCookie(tokenUrl="/api/business/auth/sign-in")


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
        raise InvalidTokenException
    current_business = await BusinessService.get_business(uuid.UUID(business_id))
    return current_business
