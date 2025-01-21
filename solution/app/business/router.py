from fastapi import APIRouter, status, Response
from pydantic import EmailStr

from solution.app.business.schemas import BusinessCreate, Business
from solution.app.business.service import BusinessService
from solution.app.exceptions import InvalidCredentialsException

router = APIRouter(prefix="/business", tags=["B2B"])


@router.post("/auth/sign-up", status_code=status.HTTP_200_OK)
async def sign_up(
        business: BusinessCreate
) -> Business:
    return await BusinessService.register_new_business(business)


@router.post("/auth/sign-in")
async def sign_in(
        response: Response,
        email: EmailStr,
        password: str
):
    business = await BusinessService.authenticate_business(email, password)
    if not business:
        raise InvalidCredentialsException
    token = await BusinessService.create_token(business.id)
    response.set_cookie(
        'access_token',
        token,
        max_age=720 * 60,
        httponly=True
    )
    return {"token": token, "company_id": business.id}
