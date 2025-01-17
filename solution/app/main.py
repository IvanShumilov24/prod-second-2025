from fastapi import FastAPI
from loguru import logger

from config import settings

app = FastAPI(title="PROOOOOOOOOOOOOOOOOD")


@app.get("/api/ping")
def send():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    logger.add("../api.log")

    host, port = settings.SERVER_ADDRESS.split(":")

    logger.info("Server is running")
    uvicorn.run("main:app")

    # host, port = settings.SERVER_ADDRESS.split(":")
    # uvicorn.run("main:app", host=host, port=int(port))

    logger.info("Server is stopped")
