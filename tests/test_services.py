import pytest
from quiz.models import Category, Question, Quiz
from quiz.services.category import CategoryService
from quiz.services.question import QuestionService
from quiz.services.quiz import QuizService


@pytest.mark.django_db
class TestCategoryService:
    def setup_method(self) -> None:
        """Подготавливает сервис"""

        self.service = CategoryService()

    def test_create_and_get_category(self, category) -> None:
        """Тест создания и получения категории"""

        fetched = self.service.get_category(category.id)
        assert fetched.title == 'Science'

    def test_update_category(self, category) -> None:
        """Тест обновления категории"""

        updated = self.service.update_category(category.id, {'title': 'New'})
        assert updated.title == 'New'

    def test_delete_category(self, category) -> None:
        """Тест удаления категории"""

        self.service.delete_category(category.id)
        assert Category.objects.count() == 0


@pytest.mark.django_db
class TestQuizService:
    def setup_method(self) -> None:
        """Подготавливает сервис"""

        self.service = QuizService()

    def test_create_and_get_category(self, quiz) -> None:
        """Тест создания и получения квиза"""

        fetched = self.service.get_quiz(quiz.id)
        assert fetched.title == 'Science'

    def test_update_quiz(self, quiz) -> None:
        """Тест обновления квиза"""

        updated = self.service.update_quiz(quiz.id, {'title': 'New'})
        assert updated.title == 'New'

    def test_delete_category(self, quiz) -> None:
        """Тест удаления квиза"""

        self.service.delete_quiz(quiz.id)
        assert Quiz.objects.count() == 0


@pytest.mark.django_db
class TestQuestionService:
    def setup_method(self) -> None:
        """Подготавливает сервис"""

        self.service = QuestionService()

    def test_create_and_get_category(self, question) -> None:
        """Тест создания и получения вопроса"""

        fetched = self.service.get_question(question.id)
        assert fetched.text == 'text'

    def test_update_question(self, question) -> None:
        """Тест обновления вопроса"""

        updated = self.service.update_question(question.id, {'text': 'New'})
        assert updated.text == 'New'

    def test_delete_question(self, question) -> None:
        """Тест удаления вопроса"""

        assert question.text == 'text'
        self.service.delete_question(question.id)
        assert Question.objects.count() == 0
