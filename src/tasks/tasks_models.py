from sqlalchemy import Column, Integer
from tasks_database import Base


class TestQuestions(Base):
    """
    Модель для создания таблицы с правильными ответами на вопросы.

    Атрибуты:
    - test_id (int): Идентификатор теста.
    - question_id (int): Идентификатор вопроса.
    - right_answer (int): Правильный ответ на вопрос.
    """
    __tablename__ = "test_questions"
    test_id = Column(Integer, primary_key=True)
    question_id = Column(Integer)
    right_answer = Column(Integer)


Base.metadata.create_all(bind=engine)
