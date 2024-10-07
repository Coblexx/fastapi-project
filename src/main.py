from fastapi import FastAPI

from src.routers import students

app = FastAPI()


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": "Hello World"}


app.include_router(students.router, prefix="/students", tags=["students"])
