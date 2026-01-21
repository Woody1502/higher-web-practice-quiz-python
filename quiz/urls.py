from django.urls import path

from quiz.views.category import CategoryDetailAPIView, CategoryListAPIView
from quiz.views.question import (QuestionByTextAPIView,
                                 QuestionCheckAnswerAPIView,
                                 QuestionDetailAPIView, QuestionListAPIView)
from quiz.views.quiz import (QuizByTitleAPIView, QuizDetailAPIView,
                             QuizListAPIView, QuizRandomQuestionAPIView)

urlpatterns = [
    path('category/', CategoryListAPIView.as_view(), name='category-list'),
    path(
        'category/<int:pk>',
        CategoryDetailAPIView.as_view(),
        name='category-detail'),
    path('questions/', QuestionListAPIView.as_view(), name='question-list'),
    path(
        'questions/<int:pk>/',
        QuestionDetailAPIView.as_view(),
        name='question-detail'),

    path('questions/by_text/<str:text>/',
         QuestionByTextAPIView.as_view(),
         name='question-by-text'),

    path('questions/<int:id>/check/',
         QuestionCheckAnswerAPIView.as_view(),
         name='question-check-answer'),
    path('quizzes/', QuizListAPIView.as_view(), name='quiz-list'),
    path('quizzes/<int:pk>/', QuizDetailAPIView.as_view(), name='quiz-detail'),


    path('quizzes/by_title/<str:title>/',
         QuizByTitleAPIView.as_view(),
         name='quiz-by-title'),

    path('quizzes/<int:id>/random_question/',
         QuizRandomQuestionAPIView.as_view(),
         name='quiz-random-question'),
]
