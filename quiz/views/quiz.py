from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from quiz.models import Quiz
from quiz.serializers import QuestionSerializer, QuizSerializer
from quiz.services.question import QuestionService
from quiz.services.quiz import QuizService


class QuizListAPIView(APIView):
    """
    Docstring для QuizListAPIView
    """

    def __init__(self) -> None:
        """
        Docstring для __init__
        """
        super().__init__()
        self.service = QuizService()
        self.serializer_class = QuizSerializer

    @swagger_auto_schema(
        operation_description='Получить список всех квизов',
        responses={
            200: QuizSerializer(many=True),
            400: 'Bad Request'
        }
    )
    def get(self, request: Request) -> Response:
        """
        Docstring для get

        :param request: Запрос
        :type request: Request
        :return: Ответ
        :rtype: Response
        """
        quizs = self.service.list_quizzes()
        serializer = self.serializer_class(quizs, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description='Создать новый квиз',
        request_body=QuizSerializer,
        responses={
            201: QuizSerializer,
            400: 'Bad Request'
        }
    )
    def post(self, request: Request) -> Response:
        """
        Docstring для get

        :param request: Запрос
        :type request: Request
        :return: Ответ
        :rtype: Response
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = self.service.create_quiz(serializer.validated_data)
            res = self.serializer_class(data)
            return Response(res.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuizDetailAPIView(APIView):
    """
    Docstring для QuizDetailAPIView
    """

    def __init__(self) -> None:
        """
        Docstring для __init__

        """
        super().__init__()
        self.service = QuizService()
        self.serializer_class = QuizSerializer

    @swagger_auto_schema(
        operation_description='Получить квиз',
        responses={
            200: QuizSerializer,
            400: 'Bad Request',
            404: 'Not found'
        }
    )
    def get(self, request: Request, pk: int) -> Response:
        """
        Docstring для get

        :param request: Запрос
        :type request: Request
        :param pk: Id
        :type pk: int
        :return: Ответ
        :rtype: Response
        """
        try:
            quiz = self.service.get_quiz(quiz_id=pk)
            serializer = self.serializer_class(quiz)
            return Response(serializer.data)
        except Quiz.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description='Обновить квиз',
        request_body=QuizSerializer,
        responses={
            200: QuizSerializer,
            400: 'Bad Request',
            404: 'Not found'
        }
    )
    def put(self, request: Request, pk: int) -> Response:
        """
        Docstring для get

        :param request: Запрос
        :type request: Request
        :param pk: Id
        :type pk: int
        :return: Ответ
        :rtype: Response
        """
        try:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                data = self.service.update_quiz(
                    quiz_id=pk, data=serializer.validated_data)
                res = self.serializer_class(data)
                return Response(res.data)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        except Quiz.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description='Удалить квиз',
        responses={
            204: QuizSerializer,
            404: 'Not found'
        }
    )
    def delete(self, request: Request, pk: int) -> Response:
        """
        Docstring для get

        :param request: Запрос
        :type request: Request
        :param pk: Id
        :type pk: int
        :return: Ответ
        :rtype: Response
        """
        try:
            self.service.delete_quiz(quiz_id=pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Quiz.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class QuizByTitleAPIView(APIView):
    """
    Docstring для QuizByTextAPIView
    """

    def __init__(self) -> None:
        """
        Docstring для __init__

        """
        super().__init__()
        self.service = QuizService()
        self.serializer_class = QuizSerializer

    @swagger_auto_schema(
        operation_description='Получить квиз по названию',
        responses={
            200: QuizSerializer(many=True),
            400: 'Bad Request'
        }
    )
    def get(self, request: Request, title: str) -> Response:
        """
        Получить квиз по названию

        :param request: Запрос
        :type request: Request
        :param text: Текст
        :type text: str
        :return: Ответ
        :rtype: Response
        """
        quiz = self.service.get_quizes_by_title(title)
        serializer = self.serializer_class(quiz, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuizRandomQuestionAPIView(APIView):
    """
    Docstring для QuizRandomQuestionAPIView
    """

    def __init__(self) -> None:
        """
        Docstring для __init__

        """
        super().__init__()
        self.service_questions = QuestionService()
        self.serializer_class = QuestionSerializer

    @swagger_auto_schema(
        operation_description='Получить квиз по названию',
        responses={
            200: QuizSerializer(many=True),
            404: 'Not found'
        }
    )
    def get(self, request: Request, id: int) -> Response:
        """
        Получение рандомного вопроса

        :param id: Id квиза
        """
        try:
            question = self.service_questions.random_question_from_quiz(
                quiz_id=id)
            serializer = self.serializer_class(question)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Quiz.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
