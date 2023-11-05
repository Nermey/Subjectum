from sqlalchemy import select, and_
from database import engine, session_factory
from models import meta_data_obj, UsersOrm


def create_tables():
    meta_data_obj.drop_all(engine)  # удаление всех таблиц перед новым запуском
    meta_data_obj.create_all(engine)  # создание всего и сразу


def add_new_user(login, password, name):
    new_user = UsersOrm(login=login, password=password, name=name)
    with session_factory() as session:
        session.add(new_user)
        session.commit()


def check_user_exist(login):
    with session_factory() as session:
        query = select(UsersOrm).filter_by(login=login)
        res = session.execute(query)
        user = res.first()
        return user != None  # лютый костыль


def get_user_authorization(login, password):
    with session_factory() as session:
        query = select(UsersOrm).filter(and_(UsersOrm.login == login,
                                             UsersOrm.password == password
                                             ))
        res = session.execute(query)
        user = res.first()
        return user != None  # такая же история
