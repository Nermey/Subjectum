from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from tasks_config_config import DATA_BASE_URL
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(DATA_BASE_URL())

session_local = async_sessionmaker(engine)


class Base(DeclarativeBase):
    pass
