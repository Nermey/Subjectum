from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from orm import Authorization

app = FastAPI()


async def create_table():
    await Authorization.create_tables()


create_table()


class User(BaseModel):
    email: str
    password: str
    name: str


class PasswordChanger(BaseModel):
    id: int
    new_password: str


class NameChanger(BaseModel):
    id: int
    new_name: str


class User_login(BaseModel):
    email: str
    password: str


@app.post("/register")
async def register(user: User):
    if await Authorization.check_user_exist(user.email):
        raise HTTPException(status_code=201, detail="user is already exist")
    await Authorization.add_new_user(user.email, user.password, user.name)
    raise HTTPException(status_code=200, detail="user is successfully added") # return user id


@app.post("/login")
async def login(user: User_login):
    if await Authorization.get_user_authorization(user.email, user.password):
        raise HTTPException(status_code=203, detail="authorization is successful")  # отправить id
    raise HTTPException(status_code=401, detail="login or password are incorrect")


@app.post("/change_password")
async def change_password(user: PasswordChanger):
    await Authorization.change_password(user.id, user.new_password)
    raise HTTPException(status_code=204, detail="password is successfully changed")  # не выводит detail


@app.post("/change_name")
async def change_password(user: NameChanger):
    await Authorization.change_password(user.id, user.new_name)
    raise HTTPException(status_code=205, detail="name is successfully changed")
