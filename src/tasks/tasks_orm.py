from test_database import session_local
from sqlalchemy import select
from tasks_models import TestQuestions


class Authorization:
    @staticmethod
    async def check_answer(test_id, question_id, user_answer):
        """
        Проверяет правильность ответа на вопрос в тесте.

        Параметры:
        - test_id: Идентификатор теста.
        - question_id: Идентификатор вопроса.
        - user_answer: Ответ пользователя.

        Возвращает:
        - True, если ответ правильный.
        - False, если ответ неправильный.
        """
        async with session_local() as session:
            query = select(TestQuestions.right_answer).filter_by(test_id=test_id, question_id=question_id)
            res = await session.execute(query)
            correct_answer = res.scalar_one_or_none()
            return correct_answer == user_answer

    @staticmethod
    async def get_total_questions(test_id):
        """
        Возвращает общее количество вопросов в тесте.

        Параметры:
        - test_id: Идентификатор теста.

        Возвращает:
        - Количество вопросов в тесте.
        """
        async with session_local() as session:
            query = select(TestQuestions.question_id).filter_by(test_id=test_id)
            res = await session.execute(query)
            total_questions = res.scalars().count()
            return total_questions
