from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from quiz.models import Question
from quiz.serializers import QuestionSerializer
from quiz.services.question import QuestionService


class QuestionListAPIView(APIView):
    """
    Docstring для QuestionListAPIView
    """

    def __init__(self) -> None:
        """
        Docstring для __init__
        """
        super().__init__()
        self.service = QuestionService()
        self.serializer_class = QuestionSerializer

    @swagger_auto_schema(
        operation_description='Получить список всех вопросов',
        responses={
            200: QuestionSerializer(many=True),
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
        questions = self.service.list_questions()
        serializer = self.serializer_class(questions, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description='Создать новый вопрос',
        request_body=QuestionSerializer,
        responses={
            201: QuestionSerializer,
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
            data = serializer.validated_data.copy()
            quiz_id = data['quiz_id'].id
            data.pop('quiz_id')
            data = self.service.create_question(quiz_id=quiz_id, data=data)
            res = self.serializer_class(data)
            return Response(res.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionDetailAPIView(APIView):
    """
    Docstring для QuestionDetailAPIView
    """

    def __init__(self) -> None:
        """
        Docstring для __init__

        """
        super().__init__()
        self.service = QuestionService()
        self.serializer_class = QuestionSerializer

    @swagger_auto_schema(
        operation_description='Получить вопрос',
        responses={
            200: QuestionSerializer,
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
            question = self.service.get_question(question_id=pk)
            serializer = self.serializer_class(question)
            return Response(serializer.data)
        except Question.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description='Обновить вопрос',
        request_body=QuestionSerializer,
        responses={
            200: QuestionSerializer,
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
                data = self.service.update_question(
                    question_id=pk, data=serializer.validated_data)
                res = self.serializer_class(data)
                return Response(res.data)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        except Question.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description='Удалить вопрос',
        responses={
            204: QuestionSerializer,
            400: 'Bad Request',
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
            self.service.delete_question(question_id=pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Question.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class QuestionByTextAPIView(APIView):
    """
    Docstring для QuestionByTextAPIView
    """

    def __init__(self) -> None:
        """
        Docstring для __init__

        """
        super().__init__()
        self.service = QuestionService()
        self.serializer_class = QuestionSerializer

    @swagger_auto_schema(
        operation_description='Получить вопрос по тексту',
        responses={
            200: QuestionSerializer(many=True),
            400: 'Bad Request'
        }
    )
    def get(self, request: Request, text: str) -> Response:
        """
        Получить вопрос по тексту

        :param request: Запрос
        :type request: Request
        :param text: Текст
        :type text: str
        :return: Ответ
        :rtype: Response
        """
        question = self.service.get_questions_by_text(text)
        serializer = self.serializer_class(question, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuestionCheckAnswerAPIView(APIView):
    """
    Docstring для QuestionCheckAnswerAPIView
    """

    def __init__(self) -> None:
        """
        Docstring для __init__

        """
        super().__init__()
        self.service = QuestionService()
        self.serializer_class = QuestionSerializer

    @swagger_auto_schema(
        operation_description='Проверка ответа',
        responses={
            200: QuestionSerializer,
            400: 'Bad Request',
            404: 'Not found'
        }
    )
    def post(self, request: Request, id: int) -> Response:
        """
        Проверка ответа

        :param id: Id вопроса
        """
        try:
            question_is_correct = self.service.check_answer(
                id, answer=request.data.get('answer'))
            return Response({'answer': question_is_correct},
                            status=status.HTTP_200_OK)
        except Question.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
