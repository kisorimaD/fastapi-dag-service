from db import LocalSession
from contextlib import asynccontextmanager
from fastapi import Depends

@asynccontextmanager
async def get_db_session():
    async with LocalSession as session:
        yield session


Session = Depends(get_db_session)