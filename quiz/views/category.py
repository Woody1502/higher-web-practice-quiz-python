from rest_framework import viewsets

from quiz.serializers import CategorySerializer
from quiz.services.category import CategoryService


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Docstring для CategoryViewSet
    """

    service = CategoryService()
    queryset = service.list_categories()
    serializer_class = CategorySerializer
    http_method_names = ['get', 'post', 'put', 'delete']
