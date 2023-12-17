from fastapi import FastAPI, HTTPException
from schemas import User, User_login, PasswordChanger, NameChanger
from orm import Authorization

Authorization.create_tables()

app = FastAPI()


@app.post("/register")
async def register(user: User):
    if await Authorization.check_user_exist(user.email):
        raise HTTPException(status_code=401, detail="User already exists")
    res = await Authorization.add_new_user(user.email, user.password, user.name)
    raise HTTPException(status_code=201, detail={"status": "user is successfully added",
                                                 "user_id": res})


@app.post("/login")
async def login(user: User_login):
    res = await Authorization.get_user_authorization(user.email, user.password)
    if res[0]:
        raise HTTPException(status_code=202, detail={"status": "authorization is successfully",
                                                     "user_id": res[1]})
    raise HTTPException(status_code=402, detail="login or password are incorrect")


@app.post("/change_password")
async def change_password(user: PasswordChanger):
    await Authorization.change_password(user.id, user.new_password)
    raise HTTPException(status_code=203, detail="Password is successfully changed")


@app.post("/change_name")
async def change_password(user: NameChanger):
    await Authorization.change_password(user.id, user.new_name)
    raise HTTPException(status_code=204, detail="Name is successfully changed")


@app.post("/test_result")
async def test_result(user_id: int):
    try:
        await app.test_client().post("/test")
    except HTTPException as e:
        if e.status_code == 200 and e.detail == "Test is passed":
            await Authorization.update_progress(user_id)
            raise HTTPException(status_code=205, detail="Test result processed")
        else:
            raise HTTPException(status_code=206, detail="Progress has not been changed")
    raise HTTPException(status_code=206, detail="Progress has not been changed")
