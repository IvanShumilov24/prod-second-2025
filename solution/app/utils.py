from datetime import datetime
from typing import Dict, Optional, Literal

from fastapi import Request
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel
from fastapi.security import OAuth2
from fastapi.security.utils import get_authorization_scheme_param
from passlib.context import CryptContext

from .exceptions import BusinessNotAuthException
from .promo.schemas import Promo

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserOAuth2PasswordBearerWithCookie(OAuth2, ):
    def __init__(
            self,
            tokenUrl: str,
            scheme_name: Optional[str] = None,
            scopes: Optional[Dict[str, str]] = None,
            auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(
            password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.cookies.get("user_access_token")

        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise BusinessNotAuthException
            else:
                return None
        return param


class BusinessOAuth2PasswordBearerWithCookie(OAuth2, ):
    def __init__(
            self,
            tokenUrl: str,
            scheme_name: Optional[str] = None,
            scopes: Optional[Dict[str, str]] = None,
            auto_error: bool = True,
    ):
        if not scopes:
            scopes = {}
        flows = OAuthFlowsModel(
            password={"tokenUrl": tokenUrl, "scopes": scopes})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        authorization: str = request.cookies.get("business_access_token")

        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                raise BusinessNotAuthException
            else:
                return None
        return param


def is_valid_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def sort_promo_list(promo_list: list[Promo], sort_by: Literal["active_from", "active_until"]) -> list[Promo]:
    def get_date(promo: Promo) -> Optional[datetime]:
        if sort_by == 'active_from':
            date_str = promo.active_from
        elif sort_by == "active_until":
            date_str = promo.active_until
        else:
            date_str = None
        if date_str:
            try:
                return date_str
            except ValueError:
                logger.error("Failed sort list promo")
        return None

    return sorted(promo_list, key=get_date)
