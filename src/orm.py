from database import Base, engine, session_local
from sqlalchemy import select
from models import Users


class Authorization:
    """
    Класс, предоставляющий методы для работы с авторизацией пользователей.
    """

    @staticmethod
    async def create_tables():
        """
        Создает таблицы в базе данных, используя метаданные модели Base.
        """
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    @staticmethod
    async def check_user_exist(email):
        """
        Проверяет, существует ли пользователь с указанным email.

        Параметры:
        - email (str): Email пользователя.

        Возвращает:
        - True, если пользователь существует.
        - False, если пользователь не существует.
        """
        async with session_local() as session:
            query = select(Users).filter_by(email=email)
            res = await session.execute(query)
            user = res.first()
            return user is not None

    @staticmethod
    async def get_user_authorization(email, password):
        """
        Проверяет авторизацию пользователя по указанному email и паролю.

        Параметры:
        - email (str): Email пользователя.
        - password (str): Пароль пользователя.

        Возвращает:
        - True, если авторизация успешна.
        - False, если авторизация неуспешна.
        """
        async with session_local() as session:
            query = select(Users).filter_by(email=email, password=password)
            res = await session.execute(query)
            user = res.first()
            return user is not None

    @staticmethod
    async def add_new_user(email, password, name):
        """
        Добавляет нового пользователя в базу данных.

        Параметры:
        - email (str): Email пользователя.
        - password (str): Пароль пользователя.
        - name (str): Имя пользователя.
        """
        async with session_local() as session:
            user_obj = Users(email=email, password=password, name=name)
            session.add(user_obj)
            await session.commit()

    @staticmethod
    async def change_password(user_id, new_password):
        """
        Изменяет пароль пользователя.

        Параметры:
        - user_id (int): Идентификатор пользователя.
        - new_password (str): Новый пароль пользователя.
        """
        async with session_local() as session:
            user = await session.get(Users, user_id)
            user.password = new_password
            await session.commit()

    @staticmethod
    async def change_name(user_id, new_name):
        """
        Изменяет имя пользователя.

        Параметры:
        - user_id (int): Идентификатор пользователя.
        - new_name (str): Новое имя пользователя.
        """
        async with session_local() as session:
            user = await session.get(Users, user_id)
            user.name = new_name
            await session.commit()

    @staticmethod
    async def update_progress(user_id):
        """
        Увеличивает прогресс пользователя.

        Параметры:
        - user_id (int): Идентификатор пользователя.
        """
        async with session_local() as session:
            user = await session.get(Users, user_id)
            user.progress += 1
            await session.commit()
