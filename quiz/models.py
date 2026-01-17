from django.db import models

from quiz.utils import (EXP_LEN, MAX_LEN, TEXT_LEN, TITLE_CAT_LEN,
                        TITLE_QUIZ_LEN)


class Category(models.Model):
    """Модель категории вопросов"""

    title = models.CharField(
        max_length=TITLE_CAT_LEN,
        null=False,
        unique=True,
        verbose_name='Имя категории')

    class Meta:
        """
        Docstring для Meta
        """

        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        """
        Docstring для __str__
        """
        return self.title[:MAX_LEN]


class Quiz(models.Model):
    """Модель квиза"""

    title = models.CharField(
        max_length=TITLE_QUIZ_LEN, null=False,
        verbose_name='Имя квиза')
    description = models.TextField(
        verbose_name='описание',
        max_length=TEXT_LEN,
        null=True,
        blank=True)

    class Meta:
        """
        Docstring для Meta
        """

        verbose_name = 'квиз'
        verbose_name_plural = 'квизы'
        ordering = ['title']

    def __str__(self):
        """
        Docstring для __str__
        """
        return self.title[:MAX_LEN]


class Difficulty(models.TextChoices):
    """Варианты сложностей для вопросов"""

    EASY = 'easy', 'Лёгкий'
    MEDIUM = 'medium', 'Средний'
    HARD = 'hard', 'Сложный'


class Question(models.Model):
    """Модель вопроса"""

    quiz_id = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        verbose_name='квиз',
    )
    category_id = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='категория',
    )
    text = models.TextField(
        verbose_name='текст вопроса',
        max_length=TEXT_LEN,
        null=False)
    description = models.TextField(
        verbose_name='описание',
        max_length=TEXT_LEN)
    options = models.JSONField(verbose_name='варианты', null=False)
    correct_answer = models.CharField(
        null=False,
        verbose_name='правильный ответ')
    explanation = models.CharField(
        max_length=EXP_LEN,
        null=True,
        verbose_name='объяснение')
    difficulty = models.CharField(
        choices=Difficulty.choices,
        null=False
    )

    class Meta:
        """
        Docstring для Meta
        """

        default_related_name = 'questions'
        verbose_name = 'вопрос'
        verbose_name_plural = 'вопросы'
