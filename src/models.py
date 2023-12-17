from sqlalchemy import MetaData, Index, Column, Integer
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

meta_data_obj = MetaData()


class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column()
    password: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()
    progress: Mapped[int] = Column(Integer) # Переменная, хранящая прогресс пользователя


index_email = Index("idx_check_login", Users.email)
index_authorization = Index("idx_authorization", Users.email, Users.password)
