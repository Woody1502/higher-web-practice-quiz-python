from rest_framework import serializers

from quiz.models import Category, Difficulty, Question, Quiz
from quiz.services.category import CategoryService
from quiz.services.quiz import QuizService
from quiz.utils import TEXT_LEN, TITLE_CAT_LEN


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий"""

    title = serializers.CharField(max_length=TITLE_CAT_LEN, required=True)

    class Meta:
        """
        Docstring для Meta
        """

        model = Category
        fields = '__all__'

    def validate_title(self, value: str) -> str:
        """
        Docstring для validate_title

        :param value: Название категории
        :return: Название категории
        """
        service = CategoryService()
        category = service.search_title(value)
        if category.exists():
            raise serializers.ValidationError(
                ['Такая категория уже есть']
            )
        return value


class QuestionSerializer(serializers.ModelSerializer):
    """Сериализатор для вопросов"""

    text = serializers.CharField(required=True)
    description = serializers.CharField(max_length=TEXT_LEN, required=True)
    options = serializers.JSONField(required=True)
    correct_answer = serializers.CharField(max_length=TEXT_LEN, required=True)
    difficulty = serializers.ChoiceField(
        choices=Difficulty.choices,
        required=True
    )

    class Meta:
        """
        Docstring для Meta
        """

        model = Question
        fields = '__all__'

    def validate_options(self, value: list) -> list:
        """
        Docstring для validate_options

        :param value: список ответов
        :return: список ответов
        """
        if not isinstance(value, list):
            raise serializers.ValidationError(['Требуется список'])
        if len(value) <= 1:
            raise serializers.ValidationError(['Нехватает вариантов ответа'])
        return value

    def validate(self, data: dict) -> dict:
        """
        Docstring для validate

        :param data: словарь с полями
        :return: словарь с полями
        """
        options = data.get('options')
        correct_answer = data.get('correct_answer')

        if correct_answer not in options:
            raise serializers.ValidationError([
                (f"Правильный ответ {correct_answer} "
                 f"должен быть одним из вариантов: {options}")
            ])
        if not (data.get('quiz_id') or data.get('category_id')):
            raise serializers.ValidationError([
                'Невозможно создать вопрос без квиза и категории'
            ])

        return data


class QuizSerializer(serializers.ModelSerializer):
    """Сериализатор для квизов"""

    title = serializers.CharField(required=True, max_length=TEXT_LEN)
    # не работает без явного указания required=False
    description = serializers.CharField(max_length=TEXT_LEN, required=False)

    class Meta:
        """
        Docstring для Meta
        """

        model = Quiz
        fields = '__all__'

    def validate_title(self, value: str) -> str:
        """
        Docstring для validate_title

        :param value: Название квиза
        :return: Название квиза
        """
        service = QuizService()
        quiz = service.search_quiz(value)
        if quiz.exists():
            raise serializers.ValidationError(
                ['Такаой квиз уже есть']
            )
        return value
