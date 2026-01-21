from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from quiz.models import Category
from quiz.serializers import CategorySerializer
from quiz.services.category import CategoryService


class CategoryListAPIView(APIView):
    """
    Docstring для CategoryViewSet
    """

    def __init__(self) -> None:
        """
        Docstring для __init__
        """
        super().__init__()
        self.service = CategoryService()
        self.serializer_class = CategorySerializer

    @swagger_auto_schema(
        operation_description='Получить список всех категорий',
        responses={
            200: CategorySerializer(many=True),
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
        categories = self.service.list_categories()
        serializer = self.serializer_class(categories, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description='Создать новую категорию',
        request_body=CategorySerializer,
        responses={
            201: CategorySerializer,
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
            data = self.service.create_category(
                serializer.validated_data['title'])
            res = self.serializer_class(data)
            return Response(res.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailAPIView(APIView):
    """
    Docstring для CategoryDetailAPIView
    """

    def __init__(self) -> None:
        """
        Docstring для __init__

        """
        super().__init__()
        self.service = CategoryService()
        self.serializer_class = CategorySerializer

    @swagger_auto_schema(
        operation_description='Получить категорию',
        responses={
            200: CategorySerializer,
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
            categories = self.service.get_category(category_id=pk)
            serializer = self.serializer_class(categories)
            return Response(serializer.data)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description='Обновить категорию',
        request_body=CategorySerializer,
        responses={
            200: CategorySerializer,
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
                data = self.service.update_category(
                    category_id=pk, data=serializer.validated_data)
                res = self.serializer_class(data)
                return Response(res.data)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description='Удалить категорию',
        responses={
            204: CategorySerializer,
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
            self.service.delete_category(category_id=pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
