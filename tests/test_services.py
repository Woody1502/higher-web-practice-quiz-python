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

    def test_create_and_get_category(self) -> None:
        """Тест создания и получения категории"""

        category = self.service.create_category('Science')
        fetched = self.service.get_category(category.id)
        assert fetched.title == 'Science'

    def test_update_category(self) -> None:
        """Тест обновления категории"""

        category = Category.objects.create(title='Old')
        updated = self.service.update_category(category.id, {'title': 'New'})
        assert updated.title == 'New'

    def test_delete_category(self) -> None:
        """Тест удаления категории"""

        category = Category.objects.create(title='Temp')
        self.service.delete_category(category.id)
        assert Category.objects.count() == 0


@pytest.mark.django_db
class TestQuizService:
    def setup_method(self) -> None:
        """Подготавливает сервис"""

        self.service = QuizService()

    def test_create_and_get_category(self) -> None:
        """Тест создания и получения квиза"""

        quiz = self.service.create_quiz({'title': 'Science',
                                         'description': 'desc'})
        fetched = self.service.get_quiz(quiz.id)
        assert fetched.title == 'Science'

    def test_update_quiz(self) -> None:
        """Тест обновления квиза"""

        quiz = Quiz.objects.create(title='Old')
        updated = self.service.update_quiz(quiz.id, {'title': 'New'})
        assert updated.title == 'New'

    def test_delete_category(self) -> None:
        """Тест удаления квиза"""

        quiz = Quiz.objects.create(title='Temp')
        self.service.delete_quiz(quiz.id)
        assert Quiz.objects.count() == 0


@pytest.mark.django_db
class TestQuestionService:
    def setup_method(self) -> None:
        """Подготавливает сервис"""

        self.service = QuestionService()
        self.quiz_service = QuizService()
        self.category_service=CategoryService()

    def test_create_and_get_category(self) -> None:
        """Тест создания и получения вопроса"""

        category = self.category_service.create_category({'title': 'Natural',
                                         'description': 'desc'})
        quiz = self.quiz_service.create_quiz({'title': 'Science',
                                         'description': 'desc'})
        question = self.service.create_question(quiz.id, data={'category_id': category,
                                                        'text': 'text',
                                                        'description': 'description',
                                                        'options': ["1", "2"],
                                                        'correct_answer': "1",
                                                        'explanation': 'explanation',
                                                        'difficulty': 'easy'
                                                        })
        fetched = self.service.get_question(question.id)
        assert fetched.text == 'text'

    def test_update_question(self) -> None:
        """Тест обновления вопроса"""

        quiz = self.quiz_service.create_quiz({'title': 'Science',
                                         'description': 'desc'})
        
        category = self.category_service.create_category({'title': 'Natural',
                                         'description': 'desc'})
        
        question = self.service.create_question(quiz.id, data={'category_id': category,
                                                        'text': 'text',
                                                        'description': 'description',
                                                        'options': ["1", "2"],
                                                        'correct_answer': "1",
                                                        'explanation': 'explanation',
                                                        'difficulty': 'easy'
                                                        })
        updated = self.service.update_question(quiz.id, {'text': 'New'})
        assert updated.text == 'New'

    def test_delete_question(self) -> None:
        """Тест удаления вопроса"""

        quiz = self.quiz_service.create_quiz({'title': 'Science',
                                         'description': 'desc'})
        
        category = self.category_service.create_category({'title': 'Natural',
                                         'description': 'desc'})
        
        question = self.service.create_question(quiz.id, data={'category_id': category,
                                                        'text': 'text',
                                                        'description': 'description',
                                                        'options': ["1", "2"],
                                                        'correct_answer': "1",
                                                        'explanation': 'explanation',
                                                        'difficulty': 'easy'
                                                        })
        assert question.text == 'text'
        self.service.delete_question(question.id)
        assert Question.objects.count() == 0
