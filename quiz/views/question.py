from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from quiz.serializers import QuestionSerializer
from quiz.services.question import QuestionService


class QuestionViewSet(viewsets.ModelViewSet):
    """
    Docstring для QuestionViewSet
    """

    service = QuestionService()
    queryset = service.list_questions()
    serializer_class = QuestionSerializer
    http_method_names = ['get', 'post', 'put', 'delete']

    @action(
        detail=False,
        methods=['get'],
        url_path=r'by_text/(?P<text>[-\w]+)',
    )
    def by_text(self, request: Request, text: str) -> Response:
        """
        Получение вопроса по тексту

        :param text: Текст вопроса
        """
        question = self.service.get_questions_by_text(text)
        serializer = self.get_serializer(question, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['post'],
        url_path=r'(?P<id>\d+)/check',
    )
    def check_answer(self, request: Request, id: int) -> Response:
        """
        Проверка ответа

        :param id: Id вопроса
        """
        question_is_correct = self.service.check_answer(
            id, answer=request.data.get('answer'))
        return Response({'answer': question_is_correct},
                        status=status.HTTP_200_OK)
