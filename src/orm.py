from database import Base, engine, session_local
from sqlalchemy import select
from models import Users


class Authorization:
    @staticmethod
    async def create_tables():
        async with engine.begin() as conn:
            #await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def check_user_exist(email):
        async with session_local() as session:
            query = select(Users).filter_by(email=email)
            res = await session.execute(query)
            user = res.scalars().all()
            print(user)
            return len(user) == 0

    @staticmethod
    async def get_user_authorization(email, password):
        async with session_local() as session:
            query = select(Users).filter_by(email=email, password=password)
            res = await session.execute(query)
            user = res.scalars().all()
            return len(user) != 0

    @staticmethod
    async def add_new_user(email, password, name):
        async with session_local() as session:
            user_obj = Users(email=email, password=password, name=name, progress=0)
            session.add(user_obj)
            await session.commit()

    @staticmethod
    async def change_password(user_id, new_password):
        async with session_local() as session:
            user = await session.get(Users, user_id)
            user.password = new_password
            await session.commit()

    @staticmethod
    async def change_name(user_id, new_name):
        async with session_local() as session:
            user = await session.get(Users, user_id)
            user.name = new_name
            await session.commit()

    @staticmethod
    async def update_progress(user_id):
        async with session_local() as session:
            user = await session.get(Users, user_id)
            user.progress += 1
            await session.commit()
