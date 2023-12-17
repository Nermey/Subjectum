from fastapi import FastAPI, HTTPException
from schemas import User, User_login, PasswordChanger, NameChanger
from orm import Authorization
import asyncio
import uvicorn


async def create_table():
    await Authorization.create_tables()


def fast_api_app():
    app = FastAPI(title="FastApi")

    @app.post("/register")
    async def register(user: User):
        if await Authorization.check_user_exist(user.email):
            raise HTTPException(status_code=201, detail="User already exists")
        await Authorization.add_new_user(user.email, user.password, user.name)
        raise HTTPException(status_code=200, detail="user is successfully added")  # return user id

    @app.post("/login")
    async def login(user: User_login):
        if await Authorization.get_user_authorization(user.email, user.password):
            raise HTTPException(status_code=203, detail="Authorization is successful")  # отправить id
        raise HTTPException(status_code=401, detail="login or password are incorrect")

    @app.post("/change_password")
    async def change_password(user: PasswordChanger):
        await Authorization.change_password(user.id, user.new_password)
        raise HTTPException(status_code=204, detail="Password is successfully changed")

    @app.post("/change_name")
    async def change_password(user: NameChanger):
        await Authorization.change_password(user.id, user.new_name)
        raise HTTPException(status_code=205, detail="Name is successfully changed")

    @app.post("/test_result")
    async def test_result(user_id: int):
        try:
            await app.test_client().post("/test")  # Проверка результата теста из /src/test/test.py
        except HTTPException as e:
            if e.status_code == 200 and e.detail == "Test is passed":
                await Authorization.update_progress(user_id)  # Если тест пройден успешно, прогресс пользователя растёт
                raise HTTPException(status_code=200, detail="Test result processed")
            else:
                raise HTTPException(status_code=200, detail="Progress has not been changed")
        raise HTTPException(status_code=200, detail="Progress has not been changed")

    return app


app = fast_api_app()

if __name__ == "__main__":
    asyncio.run(create_table())
    uvicorn.run(
        app="src.auth:app",
        host="localhost",
        port=6100
    )
