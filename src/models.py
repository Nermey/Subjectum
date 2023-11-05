from sqlalchemy import Table, Column, INTEGER, String, MetaData, Index
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

meta_data_obj = MetaData()

users_table = Table(
    "users",
    meta_data_obj,
    Column("id", INTEGER, primary_key=True),
    Column("login", String),
    Column("password", String),
    Column("name", String),
)

index_login = Index("idx_check_login", users_table.c.login)
index_authorization = Index("idx_authorization", users_table.c.login, users_table.c.password)


class UsersOrm(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()
