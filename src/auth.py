from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from orm import Authorization


app = FastAPI()
Authorization.create_tables()


class User(BaseModel):
    email: str
    password: str
    name: str


class User_login(BaseModel):
    email: str
    password: str


@app.post("/register")
async def register(user: User):
    if await Authorization.check_user_exist(user.email):
        raise HTTPException(status_code=201, detail="user is already exist")
    await Authorization.add_new_user(user.email, user.password, user.name)
    raise HTTPException(status_code=200, detail="user is successfully added")


@app.post("/login")
async def login(user: User_login):
    if await Authorization.get_user_authorization(user.email, user.password):
        raise HTTPException(status_code=203, detail="authorization is successful")
    raise HTTPException(status_code=203, detail="login or password are incorrect")
