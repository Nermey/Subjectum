from pydantic import BaseModel


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


class UserDTO(User):
    id: int
