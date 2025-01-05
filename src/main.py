import logging

from fastapi import FastAPI

from src.routers import students

app = FastAPI()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.info("Logger initialized")


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello World"}


app.include_router(students.router, prefix="/students", tags=["students"])
