from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from quiz.serializers import QuestionSerializer, QuizSerializer
from quiz.services.question import QuestionService
from quiz.services.quiz import QuizService


class QuizViewSet(viewsets.ModelViewSet):
    """
    Docstring для QuizViewSet
    """

    service = QuizService()
    service_questions = QuestionService()
    queryset = service.list_quizzes()
    serializer_class = QuizSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

    @action(
        detail=False,
        methods=['get'],
        url_path=r'by_title/(?P<title>[-\w]+)',
    )
    def by_title(self, request: Request, title: str) -> Response:
        """
        Получение квиза по названию

        :param title: Название
        """
        quiz = self.service.get_quizes_by_title(title)
        serializer = self.get_serializer(quiz, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['get'],
        url_path=r'(?P<id>\d+)/random_question',
    )
    def random_question(self, request: Request, id: int) -> Response:
        """
        Получение рандомного вопроса

        :param id: Id квиза
        """
        question = self.service_questions.random_question_from_quiz(id)
        serializer = QuestionSerializer(question)
        return Response(serializer.data, status=status.HTTP_200_OK)
