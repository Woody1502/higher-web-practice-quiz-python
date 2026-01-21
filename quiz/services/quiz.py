from quiz.dao import AbstractQuizService
from quiz.models import Quiz
from quiz.services.utils import update_model


class QuizService(AbstractQuizService):
    """Реализация сервиса для квиза"""

    def list_quizzes(self) -> list[Quiz]:
        """Возвращает список всех квизов."""
        return Quiz.objects.all()

    def get_quiz(self, quiz_id: int) -> Quiz:
        """
        Возвращает квиз по его идентификатору.

        :param quiz_id: Идентификатор квиза.
        :return: Квиз из БД.
        """
        return Quiz.objects.get(id=quiz_id)

    def get_quizes_by_title(self, title: str) -> list[Quiz]:
        """
        Возвращает список квизов по названию.

        :param title: Название квиза.
        :return: Список квизов с подходящими названиями.
        """
        return Quiz.objects.filter(title__contains=title)

    def create_quiz(self, data: dict) -> Quiz:
        """
        Создает новый квиз.

        :param data: Данные из запроса для создания квиза.
        :return: Созданный квиз.
        """
        return Quiz.objects.create(**data)

    def update_quiz(self, quiz_id: int, data: dict) -> Quiz:
        """
        Обновляет существующий квиз.

        :param quiz_id: Идентификатор квиза.
        :param data: Данные для обновления квиза.
        :return: Обновленный квиз.
        """
        return update_model(Quiz, quiz_id, data)

    def delete_quiz(self, quiz_id: int) -> None:
        """
        Удаляет квиз по его идентификатору.

        :param quiz_id: Идентификатор квиза для удаления.
        """
        Quiz.objects.get(id=quiz_id).delete()

    def search_quiz(self, title: str) -> list[Quiz]:
        """
        Ищет квиз с названием title

        :param title: Название квиза
        :return: queryset с 1 объектом
        """
        return Quiz.objects.filter(title__icontains=title)
