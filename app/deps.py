from .db import LocalSession
from contextlib import asynccontextmanager
from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

@asynccontextmanager
async def get_db_session():
    async with LocalSession as session:
        yield session


Session = Annotated[AsyncSession, Depends(get_db_session)]