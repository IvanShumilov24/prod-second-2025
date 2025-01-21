from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from loguru import logger
from pydantic import ValidationError
from starlette.responses import JSONResponse

from business.router import router as business_router
from config import settings
from solution.app.exceptions import BusinessExistsException

app = FastAPI(title="PROOOOOOOOOOOOOOOOOD")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                        content={"status": "error", "message": "Ошибка в данных запроса."})


@app.exception_handler(BusinessExistsException)
async def business_exists_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(status_code=status.HTTP_409_CONFLICT,
                        content={"status": "error", "message": "Такой email уже зарегистрирован."})


@app.get("/api/ping")
def send():
    return {"status": "ok"}


app.include_router(business_router)

if __name__ == "__main__":
    import uvicorn

    logger.add("../api.log")

    host, port = settings.SERVER_ADDRESS.split(":")

    logger.info("Server is running")
    uvicorn.run("main:app")

    # host, port = settings.SERVER_ADDRESS.split(":")
    # uvicorn.run("main:app", host=host, port=int(port))

    logger.info("Server is stopped")
