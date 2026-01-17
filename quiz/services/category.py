from quiz.dao import AbstractCategoryService
from quiz.models import Category


class CategoryService(AbstractCategoryService):
    """Реализация сервиса для категорий"""

    def list_categories(self) -> list[Category]:
        """Метод для получения списка категорий"""
        return Category.objects.all()

    def get_category(self, category_id: int) -> Category:
        """
        Метод для получения категории по идентификатору.

        :param category_id: Идентификатор категории.
        :return: Категория из БД.
        """
        return Category.objects.get(id=category_id)

    def create_category(self, title: str) -> Category:
        """
        Создает категорию вопросов.

        :param title: Название для категории.
        :return: Созданная категория.
        """
        return Category.objects.create(title=title)

    def update_category(self, category_id: int, data: dict) -> Category:
        """
        Обновляет категорию новыми данными.

        :param category_id: Идентификатор категории.
        :param data: Данные для обновления категории.
        :return: Обновленная категория.
        """
        Category.objects.filter(id=category_id).update(**data)
        return Category.objects.get(id=category_id)

    def delete_category(self, category_id: int) -> None:
        """
        Удаляет категорию.

        :param category_id: Идентификатор категории для удаления.
        """
        Category.objects.get(id=category_id).delete()

    def search_title(self, title: str) -> list[Category]:
        """
        Ищет категорию с названием title

        :param title: Название категории
        :return: queryset с 1 объектом
        """
        return Category.objects.filter(
            title=title
        )
