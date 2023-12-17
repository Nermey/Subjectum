from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import DATA_BASE_URL, SYNC_DATA_BASE_URL
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine

engine = create_async_engine(DATA_BASE_URL())
sync_engine = create_engine(SYNC_DATA_BASE_URL())

session_local = async_sessionmaker(engine)


class Base(DeclarativeBase):
    pass
