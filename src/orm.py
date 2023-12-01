from sqlalchemy import select, and_
from database import engine, session_local
from models import meta_data_obj, Users


def create_tables(): # где создавать таблицы?
    meta_data_obj.drop_all(engine)
    meta_data_obj.create_all(engine)


def add_new_user(login, password, name): # передавать pydantic model
    new_user = Users(login=login, password=password, name=name)
    with session_local() as session:
        session.add(new_user)
        session.commit()


def check_user_exist(login):
    with session_local() as session:
        query = select(Users).filter_by(login=login)
        res = session.execute(query)
        user = res.first()
        return user is None  # лютый костыль


def get_user_authorization(login, password):
    with session_local() as session:
        query = select(Users).filter(and_(Users.login == login,
                                             Users.password == password
                                             ))
        res = session.execute(query)
        user = res.first()
        return user is None  # такая же история
