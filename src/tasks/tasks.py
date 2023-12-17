from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from tasks_orm_orm import Authorization

app = FastAPI()


async def create_table():
    """
    Создает таблицы в базе данных, используя модель Authorization.
    """
    await Authorization.create_tables()


create_table()


@app.post("/test")
async def test(test_id: int, question_id: int, answer_number: int):
    """
    Проверяет результаты теста и возвращает соответствующий HTTP-ответ.

    Параметры:
    - test_id (int): Идентификатор теста.
    - question_id (int): Идентификатор вопроса.
    - answer_number (int): Номер правильного ответа.

    Возвращает:
    - Если тест пройден успешно (процент прохождения >= 80):
      - HTTP-ответ со статусом 200 и деталями "Test is passed".
    - Если тест не пройден успешно (процент прохождения < 80):
      - HTTP-ответ со статусом 200 и деталями "Test is not passed".
    """
    # Проверка на правильность ответа
    is_correct = await Authorization.check_answer(test_id, question_id, answer_number)

    # Счётчик правильных ответов
    num_correct_answers = 0
    if is_correct:
        num_correct_answers += 1

    # Количество вопросов
    total_questions = await Authorization.get_total_questions(test_id)

    # Процент прохождения теста
    pass_percentage = (num_correct_answers / total_questions) * 100

    # Отправление HTTP запроса в результате от успеха сдачи теста
    if pass_percentage >= 80:
        raise HTTPException(status_code=200, detail="Test is passed")
    else:
        raise HTTPException(status_code=200, detail="Test is not passed")
