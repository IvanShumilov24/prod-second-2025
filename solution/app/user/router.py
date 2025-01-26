from app.user.dependencies import get_current_user
from app.user.models import UserModel
from app.user.schemas import UserCreate, UserAuthResponse, User, UserUpdate
from app.user.service import UserService
from fastapi import APIRouter, status, Depends
from pydantic import EmailStr, UUID4
from starlette.responses import Response
from typing_extensions import Literal

from app.promo.schemas import PromoForUser
from app.promo.service import PromoService

router = APIRouter(prefix='/user', tags=['B2C'])


@router.post("/auth/sign-up", status_code=status.HTTP_200_OK)
async def sign_up(response: Response, user: UserCreate) -> UserAuthResponse:
    db_user = await UserService.register_new_user(user)
    token = await UserService.create_token(db_user.id)
    response.set_cookie(
        'user_access_token',
        token,
        max_age=720 * 60,
        httponly=True
    )
    return UserAuthResponse(token=token)


@router.post("/auth/sign-in")
async def sign_in(response: Response, email: EmailStr, password: str) -> UserAuthResponse:
    user = await UserService.authenticate_user(email, password)
    if not user:
        raise InvalidCredentialsException
    token = await UserService.create_token(user.id)
    response.set_cookie(
        'user_access_token',
        token,
        max_age=720 * 60,
        httponly=True
    )
    return UserAuthResponse(token=token)


@router.get("/profile")
async def get_profile(current_user: UserModel = Depends(get_current_user)) -> User:
    return current_user


@router.patch("/profile")
async def update_profile(user: UserUpdate, current_user: UserModel = Depends(get_current_user)) -> User:
    return await UserService.update_user(current_user.id, user)


@router.get("/feed")
async def get_feed(response: Response, active: bool | Literal[True, False, None] = None, category: str = None,
                   limit: int = 10, offset: int = 0, current_user: UserModel = Depends(get_current_user)) -> list[
    PromoForUser]:
    promo_list = await PromoService.get_all_promo_by_user(limit=limit, offset=offset, active=active, category=category)
    response.headers["X-Total-Count"] = str(len(promo_list))
    return promo_list


@router.get("/promo/{id}")
async def get_promo(id: UUID4, current_user: UserModel = Depends(get_current_user)) -> PromoForUser:
    promo = await PromoService.get_promo_by_user(id)
    return promo
