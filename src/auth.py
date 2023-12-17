from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from orm import Authorization

app = FastAPI()


async def create_table():
    """
    Создает таблицы в базе данных, используя модель Authorization.
    """
    await Authorization.create_tables()


create_table()


class User(BaseModel):
    """
    Модель данных для регистрации нового пользователя.
    """
    email: str
    password: str
    name: str


class PasswordChanger(BaseModel):
    """
    Модель данных для изменения пароля пользователя.
    """
    id: int
    new_password: str


class NameChanger(BaseModel):
    """
    Модель данных для изменения имени пользователя.
    """
    id: int
    new_name: str


class User_login(BaseModel):
    """
    Модель данных для входа пользователя.
    """
    email: str
    password: str


@app.post("/register")
async def register(user: User):
    """
    Регистрирует нового пользователя.

    Параметры:
    - user (User): Данные нового пользователя.

    Возвращает:
    - Если пользователь успешно зарегистрирован:
      - HTTP-ответ со статусом 200 и деталями "User is successfully added".
    - Если пользователь уже существует:
      - HTTP-ответ со статусом 201 и деталями "User already exists".
    """
    if await Authorization.check_user_exist(user.email):
        raise HTTPException(status_code=201, detail="User already exists")
    await Authorization.add_new_user(user.email, user.password, user.name)
    raise HTTPException(status_code=200, detail="User is successfully added")


@app.post("/login")
async def login(user: User_login):
    """
    Авторизует пользователя.

    Параметры:
    - user (User_login): Данные для входа пользователя.

    Возвращает:
    - Если авторизация успешна:
      - HTTP-ответ со статусом 203 и деталями "Authorization is successful".
    - Если логин или пароль некорректны:
      - HTTP-ответ со статусом 401 и деталями "login or password are incorrect".
    """
    if await Authorization.get_user_authorization(user.email, user.password):
        raise HTTPException(status_code=203, detail="Authorization is successful")
    raise HTTPException(status_code=401, detail="login or password are incorrect")


@app.post("/change_password")
async def change_password(user: PasswordChanger):
    """
    Изменяет пароль пользователя.

    Параметры:
    - user (PasswordChanger): Данные для изменения пароля.

    Возвращает:
    - Если пароль успешно изменен:
      - HTTP-ответ со статусом 204 и деталями "Password is successfully changed".
    """
    await Authorization.change_password(user.id, user.new_password)
    raise HTTPException(status_code=204, detail="Password is successfully changed")


@app.post("/change_name")
async def change_password(user: NameChanger):
    """
    Изменяет имя пользователя.

    Параметры:
    - user (NameChanger): Данные для изменения имени.

    Возвращает:
    - Если имя успешно изменено:
      - HTTP-ответ со статусом 205 и деталями "Name is successfully changed".
    """
    await Authorization.change_password(user.id, user.new_name)
    raise HTTPException(status_code=205, detail="Name is successfully changed")


@app.post("/test_result")
async def test_result(user_id: int):
    """
    Обрабатывает результаты теста.

    Параметры:
    - user_id (int): Идентификатор пользователя.

    Возвращает:
    - Если результаты теста успешно обработаны:
      - HTTP-ответ со статусом 200 и деталями "Test result processed".
    - Если прогресс пользователя не изменился:
      - HTTP-ответ со статусом 200 и деталями "Progress has not been changed".
    """
    try:
        await app.test_client().post("/test")  # Проверка результата теста из /src/test/test.py
    except HTTPException as e:
        if e.status_code == 200 and e.detail == "Test is passed":
            await Authorization.update_progress(user_id)  # Если тест пройден успешно, прогресс пользователя растёт
            raise HTTPException(status_code=200, detail="Test result processed")
        else:
            raise HTTPException(status_code=200, detail="Progress has not been changed")
    raise HTTPException(status_code=200, detail="Progress has not been changed")
