from sqlalchemy import create_engine
from config import DATA_BASE_URL
from sqlalchemy.orm import sessionmaker, DeclarativeBase

engine = create_engine(DATA_BASE_URL())

session_local = sessionmaker(engine)


class Base(DeclarativeBase):
    pass
