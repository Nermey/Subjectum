from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import select, and_

from database import session_local, engine
from models import Users, Base

app = FastAPI()
# Base.metadata.drop_all(engine)
Base.metadata.create_all(engine)


class User(BaseModel):
    email: str
    password: str
    name: str


class User_login(BaseModel):
    email: str
    password: str


@app.post("/register")
def register(user: User):
    with session_local() as session:
        user_obj = Users(email=user.email, password=user.password, name=user.name)
        if check_user_exist(user.email):
            session.add(user_obj)
            session.commit()
            raise HTTPException(status_code=200, detail="user is added successfully")
    raise HTTPException(status_code=201, detail="user is already exist")


@app.post("/login")
def login(user: User_login):
    if check_user_exist(user.email):
        raise HTTPException(status_code=202, detail="user is not exist")
    if get_user_authorization(user.email, user.password):
        raise HTTPException(status_code=203, detail="authorization is successful")
    raise HTTPException(status_code=400, detail="login or password are incorrect")


def check_user_exist(email):
    with session_local() as session:
        query = select(Users).filter_by(email=email)
        res = session.execute(query)
        user = res.first()
        return user is None


def get_user_authorization(email, password):
    with session_local() as session:
        query = select(Users).filter_by(email=email, password=password)
        res = session.execute(query)
        user = res.first()
        return user is not None
