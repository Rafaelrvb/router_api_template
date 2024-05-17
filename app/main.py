from fastapi import Depends, FastAPI
from .dependencies import get_token_header
from .routers import students, courses

app = FastAPI(dependencies=[Depends(get_token_header)])


app.include_router(students.router)
app.include_router(courses.router)


@app.get("/")
async def root():
    return {"status": "ok"}
