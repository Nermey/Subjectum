from database import Base, session_local, sync_engine
from sqlalchemy import select
from models import Users
from schemas import UserDTO


class Authorization:
    @staticmethod
    def create_tables():
        Base.metadata.create_all(sync_engine)

    @staticmethod
    async def check_user_exist(email):
        async with session_local() as session:
            query = select(Users).filter_by(email=email)
            res = await session.execute(query)
            user = res.scalars().all()
            return len(user) != 0

    @staticmethod
    async def get_user_authorization(email, password):
        async with session_local() as session:
            query = select(Users).filter_by(email=email, password=password)
            res = await session.execute(query)
            user = res.scalars().all()
            print(user)
            user_dto = [UserDTO.model_validate(row, from_attributes=True) for row in user]
            print(user_dto[0].id)
            return [len(user) != 0, user_dto[0].id]

    @staticmethod
    async def add_new_user(email, password, name):
        async with session_local() as session:
            user_obj = Users(email=email, password=password, name=name, progress=0)
            session.add(user_obj)
            await session.commit()
            await session.refresh(user_obj)
            return user_obj.id

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
