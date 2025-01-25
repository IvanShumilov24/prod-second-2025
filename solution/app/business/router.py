from typing import Literal

from fastapi import APIRouter, status, Response
from fastapi.params import Depends
from pydantic import EmailStr, UUID4

from solution.app.business.dependencies import get_current_business
from solution.app.business.schemas import BusinessCreate, BusinessAuthResponse, Business
from solution.app.business.service import BusinessService
from solution.app.exceptions import InvalidCredentialsException
from solution.app.promo.schemas import PromoCreate, PromoCreatedResponse, Promo, PromoUpdate
from solution.app.promo.service import PromoService

router = APIRouter(prefix="/business", tags=["B2B"])


@router.post("/auth/sign-up", status_code=status.HTTP_200_OK)
async def sign_up(
        response: Response,
        business: BusinessCreate
) -> BusinessAuthResponse:
    db_business = await BusinessService.register_new_business(business)
    token = await BusinessService.create_token(db_business.id)
    response.set_cookie(
        'business_access_token',
        token,
        max_age=720 * 60,
        httponly=True
    )
    return BusinessAuthResponse(token=token, company_id=db_business.id)


@router.post("/auth/sign-in")
async def sign_in(
        response: Response,
        email: EmailStr,
        password: str
) -> BusinessAuthResponse:
    business = await BusinessService.authenticate_business(email, password)
    if not business:
        raise InvalidCredentialsException
    token = await BusinessService.create_token(business.id)
    response.set_cookie(
        'business_access_token',
        token,
        max_age=720 * 60,
        httponly=True
    )
    return BusinessAuthResponse(token=token, company_id=business.id)


@router.post("/promo", status_code=status.HTTP_201_CREATED)
async def create_promo(promo: PromoCreate, business: Business = Depends(get_current_business)) -> PromoCreatedResponse:
    promo_id = await PromoService.create_promo(business, promo)
    return PromoCreatedResponse(id=promo_id)


@router.get("/promo")
async def get_promo_list(response: Response,
                         sort_by: Literal["active_from", "active_until"],
                         limit: int = 10,
                         offset: int = 0,
                         business: Business = Depends(get_current_business)) -> list[Promo]:
    promo_list = await PromoService.get_all_promo(business, limit=limit, offset=offset, sort_by=sort_by)
    response.headers["X-Total-Count"] = str(len(promo_list))
    return promo_list


@router.get("/promo/{id}")
async def get_promo(promo_id: UUID4, business: Business = Depends(get_current_business)) -> Promo:
    promo = await PromoService.get_promo(business, promo_id)
    return promo


@router.patch("/promo/{id}")
async def update_promo(promo_id: UUID4, new_promo: PromoUpdate,
                       business: Business = Depends(get_current_business)) -> Promo:
    bd_promo = await PromoService.update_promo(business, promo_id, new_promo)
    return bd_promo
