from django.contrib import admin
from django.db.models import Count, Q, QuerySet
from rest_framework.request import Request

from quiz.utils import MAX_LEN

from .models import Category, Question, Quiz


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Админка для категорий"""

    list_display = ('id', 'title', 'question_count')
    list_display_links = ('id', 'title')
    list_per_page = 20

    readonly_fields = ('question_count',)

    def get_queryset(self, request: Request) -> QuerySet:
        """Запрос с аннотацией количества вопросов"""
        queryset = super().get_queryset(request)
        return queryset.annotate(question_count=Count('questions'))

    @admin.display(
        description='Количество вопросов',
    )
    def question_count(self, obj: Category) -> int:
        """Количество вопросов в категории"""
        return obj.question_count


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    """Админка для квизов"""

    list_display = ('id', 'title', 'description_short', 'question_count',
                    'difficulty_stats')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'description')
    list_per_page = 20

    readonly_fields = ('question_count', 'difficulty_stats')

    def get_queryset(self, request: Request) -> QuerySet:
        """Запрос с аннотацией количества вопросов"""
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('questions').annotate(
            question_count=Count('questions'),
            easy_count=Count(
                'questions', filter=Q(
                    questions__difficulty='easy')),
            medium_count=Count(
                'questions', filter=Q(
                    questions__difficulty='medium')),
            hard_count=Count(
                'questions', filter=Q(
                    questions__difficulty='hard'))
        )

    @admin.display(
        description='Описание',
    )
    def description_short(self, obj: Quiz) -> str:
        """Короткое описание"""
        if obj.description and len(obj.description) > MAX_LEN:
            return f'{obj.description[:MAX_LEN]}'
        return obj.description or '-'

    @admin.display(
        description='Количество вопросов',
    )
    def question_count(self, obj: Quiz) -> int:
        """Количество вопросов в квизе"""
        return obj.question_count

    @admin.display(
        description='сложность',
    )
    def difficulty_stats(self, obj: Quiz) -> str:
        """Статистика по сложности вопросов"""
        return f'{obj.easy_count}/{obj.medium_count}/{obj.hard_count}'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Админка для вопросов"""

    list_display = ('id', 'text_short', 'category', 'quiz', 'difficulty',
                    'options_count', 'correct_answer_short', 'options_display')
    list_display_links = ('id', 'text_short', )
    search_fields = ('text', 'description', 'explanation',
                     'category_id__title', 'quiz_id__title')
    list_filter = ('difficulty', 'category_id', 'quiz_id')

    list_per_page = 20
    list_select_related = ('category_id', 'quiz_id')

    readonly_fields = ('options_display', )

    def get_queryset(self, request: Request) -> QuerySet:
        """Запрос с JOIN"""
        queryset = super().get_queryset(request)
        return queryset.select_related('category_id', 'quiz_id')

    @admin.display(
        description='Текст вопроса',
    )
    def text_short(self, obj: Question) -> str:
        """Короткий текст вопроса"""
        if obj.text and len(obj.text) > MAX_LEN:
            return f'{obj.text[:MAX_LEN]}'
        return obj.text

    @admin.display(
        description='Категория',
    )
    def category(self, obj: Question) -> str:
        """Категория"""
        return obj.category_id.title

    @admin.display(
        description='Квиз',
    )
    def quiz(self, obj: Question) -> str:
        """Квиз"""
        return obj.quiz_id.title

    @admin.display(
        description='Количество вариантов',
    )
    def options_count(self, obj: Question) -> int:
        """Количество вариантов ответа"""
        return len(obj.options)

    @admin.display(
        description='Правильный ответ',
    )
    def correct_answer_short(self, obj: Question) -> str:
        """Правильный ответ"""
        if obj.correct_answer and len(obj.correct_answer) > MAX_LEN:
            return f'{obj.correct_answer[:MAX_LEN]}...'
        return obj.correct_answer

    @admin.display(
        description='Варианты ответов',
    )
    def options_display(self, obj: Question) -> list[Question]:
        """Варианты ответов"""

        return list(obj.options)
