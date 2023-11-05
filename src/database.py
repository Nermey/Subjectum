from sqlalchemy import create_engine
from config import DATA_BASE_URL
from sqlalchemy.orm import Session, sessionmaker, DeclarativeBase

engine = create_engine(DATA_BASE_URL())  # создание машины соединения

session_factory = sessionmaker(engine)


class Base(DeclarativeBase):
    pass
