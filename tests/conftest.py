from django.urls import reverse
import pytest
from django.test import Client
from rest_framework.test import APIClient
from quiz.services.question import QuestionService
from quiz.services.quiz import QuizService
from quiz.services.category import CategoryService
from quiz.models import Category, Question, Quiz


@pytest.fixture
def category():
    """Категория"""
    return Category.objects.create(
        title='Science',
    )

@pytest.fixture
def quiz():
    """Квиз"""
    return Quiz.objects.create(
        title='Science',
        description='desc'
    )

@pytest.fixture
def question():
    """Вопрос"""
    service = QuestionService()
    category = Category.objects.create(
        title='Science',
    )
    quiz = Quiz.objects.create(
        title='Science',
        description='desc'
    )
    return service.create_question(quiz.id, data={'category_id': category,
                                                      'text': 'text',
                                                      'description': 'description',
                                                      'options': ["1", "2"],
                                                      'correct_answer': "1",
                                                      'explanation': 'explanation',
                                                      'difficulty': 'easy'
                                                      })

@pytest.fixture
def category_create_get_url():
    """URL для category-list"""
    return reverse('category-list')

@pytest.fixture
def quiz_create_get_url():
    """URL для quiz-list"""
    return reverse('quiz-list')

@pytest.fixture
def question_create_get_url():
    """URL для question-list"""
    return reverse('question-list')

@pytest.fixture
def question_response():
    """Response для question"""
    client=Client()
    response = client.post(
            reverse('quiz-list'),
            {'title': 'History of country',
             'description': 'description'},
            content_type='application/json'
        )
    quiz_id = response.json()['id']
    response = client.post(
            reverse('category-list'),
            {'title': 'History',
             'description': 'description'},
            content_type='application/json'
        )
    category_id = response.json()['id']
    return client.post(
            reverse('question-list'),
            {'quiz_id': quiz_id,
             'category_id': category_id,
             'text': 'text',
             'description': 'description',
             'options': ["1", "2"],
             'correct_answer': "1",
             'explanation': 'explanation',
             'difficulty': 'easy'
             },
            content_type='application/json'
        )