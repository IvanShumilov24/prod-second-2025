from fastapi import APIRouter, status, Depends
from pydantic import EmailStr
from starlette.responses import Response

from solution.app.user.dependencies import get_current_user
from solution.app.user.models import UserModel
from solution.app.user.schemas import UserCreate, UserAuthResponse, User, UserUpdate
from solution.app.user.service import UserService

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
