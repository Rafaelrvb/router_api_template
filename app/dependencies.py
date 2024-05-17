from .database.db import connect_db
from typing import Annotated
from fastapi import Header, HTTPException


async def get_token_header(token: Annotated[str, Header()]):
    if token != "my_token":
        raise HTTPException(status_code=400, detail="Token header invalid")


async def get_db():
    db = connect_db()
    try:
        yield db
    finally:
        db.close()
