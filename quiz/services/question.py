from quiz.dao import AbstractQuestionService
from quiz.models import Question, Quiz


class QuestionService(AbstractQuestionService):
    """Реализация сервиса для вопросов"""

    def list_questions(self) -> list[Question]:
        """
        Возвращает список всех вопросов.

        :return: Список вопросов.
        """
        return Question.objects.all()

    def get_question(self, question_id: int) -> Question:
        """
        Возвращает вопрос по его идентификатору.

        :param question_id: Идентификатор вопроса.
        :return: Вопрос из БД.
        """

        return Question.objects.get(id=question_id)

    def get_questions_by_text(self, text: str) -> list[Question]:
        """
        Возвращает вопрос по его тексту.

        :param text: Текст вопроса.
        :return: Вопрос из БД.
        """
        return Question.objects.filter(text__icontains=text)

    def get_questions_for_quiz(self, quiz_id: int) -> list[Question]:
        """
        Получение вопросов по идентификатору квиза.

        :param quiz_id: Идентификатор квиза.
        :return: Список вопросов квиза.
        """
        return Quiz.objects.get(id=quiz_id).questions.all()

    def create_question(self, quiz_id: int, data: dict) -> Question:
        """
        Создает новый вопрос.

        :param quiz_id: Идентификатор квиза, к которому относится вопрос.
        :param data: Данные из запроса для создания вопроса.
        :return: Созданный вопрос.
        """
        return Quiz.objects.get(id=quiz_id).questions.create(**data)

    def update_question(self, question_id: int, data: dict) -> Question:
        """
        Обновляет существующий вопрос.

        :param question_id: Идентификатор вопроса.
        :param data: Данные для обновления вопроса.
        :return: Обновленный вопрос.
        """
        Question.objects.update(**data)
        return Question.objects.get(id=question_id)

    def delete_question(self, question_id: int) -> None:
        """
        Удаляет вопрос по его идентификатору.

        :param question_id: Идентификатор вопроса для удаления.
        """
        return Question.objects.get(id=question_id).delete()

    def check_answer(self, question_id: int, answer: str) -> bool:
        """
        Проверяет ответ на вопрос.

        :param question_id: Идентификатор вопроса.
        :param answer: Ответ пользователя.
        :return: True, если ответ правильный, False - в противном случае.
        """
        return Question.objects.get(id=question_id).correct_answer == answer

    def random_question_from_quiz(self, quiz_id: int) -> Question:
        """
        Возвращает случайный вопрос из указанного квиза.

        :param quiz_id: Идентификатор квиза.
        :return: Случайный вопрос из квиза.
        """
        return Quiz.objects.get(id=quiz_id).questions.order_by('?').first()
