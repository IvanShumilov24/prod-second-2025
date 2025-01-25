from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from loguru import logger
from pydantic import ValidationError
from starlette.responses import JSONResponse

from business.router import router as business_router
from config import settings
from solution.app.exceptions import BusinessExistsException, InvalidCredentialsException, BusinessNotAuthException, \
    PromoNotFoundException, PromoNotBelongBusinessException, UserExistsException
from user.router import router as user_router

app = FastAPI(title="PROOOOOOOOOOOOOOOOOD")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                        content={"status": "error", "message": "Ошибка в данных запроса."})


@app.exception_handler(UserExistsException)
@app.exception_handler(BusinessExistsException)
async def business_exists_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(status_code=status.HTTP_409_CONFLICT,
                        content={"status": "error", "message": "Такой email уже зарегистрирован"})


@app.exception_handler(InvalidCredentialsException)
async def invalid_credentials_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                        content={"status": "error", "message": "Неверный email или пароль."})


@app.exception_handler(BusinessNotAuthException)
async def business_not_auth_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                        content={
                            "status": "error",
                            "message": "Пользователь не авторизован."
                        })


@app.exception_handler(PromoNotFoundException)
async def promo_not_found_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                        content={
                            "status": "error",
                            "message": "Промокод не найден."
                        })


@app.exception_handler(PromoNotBelongBusinessException)
async def promo_not_belong_business(request: Request, exc: ValidationError):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                        content={
                            "status": "error",
                            "message": "Промокод не принадлежит этой компании."
                        })


@app.get("/api/ping")
def send() -> str:
    return "PROOOOOOOOOOOOOOOOOD"


app.include_router(business_router, prefix="/api")
app.include_router(user_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn

    logger.add("../api.log")

    host, port = settings.SERVER_ADDRESS.split(":")

    logger.info("Server is running")
    uvicorn.run("main:app")

    # host, port = settings.SERVER_ADDRESS.split(":")
    # uvicorn.run("main:app", host=host, port=int(port))

    logger.info("Server is stopped")
