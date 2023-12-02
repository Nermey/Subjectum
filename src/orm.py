from database import Base, engine, session_local
from models import Users
from sqlalchemy import select


class Authorization:
    @staticmethod
    async def create_tables():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def check_user_exist(email):
        async with session_local() as session:
            query = select(Users).filter_by(email=email)
            res = await session.execute(query)
            user = res.first()
            return user is not None

    @staticmethod
    async def get_user_authorization(email, password):
        async with session_local() as session:
            query = select(Users).filter_by(email=email, password=password)
            res = await session.execute(query)
            user = res.first()
            return user is not None

    @staticmethod
    async def add_new_user(email, password, name):  # нужно ли импортировать класс User из auth (pydantic)
        async with session_local() as session:
            user_obj = Users(email=email, password=password, name=name)
            session.add(user_obj)
            await session.commit()
