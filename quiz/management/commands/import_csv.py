import ast
import os
from argparse import ArgumentParser

import pandas as pd
from django.core.management.base import BaseCommand

from quiz.models import Category, Question, Quiz


class Command(BaseCommand):

    def add_arguments(self, parser: ArgumentParser) -> None:
        """
        Docstring для add_arguments

        :param parser: аргумент
        """
        parser.add_argument('path', type=str)

    def handle(self, *args: list, **kwargs: dict) -> None:
        """
        Docstring для handle
        """
        directory_path = kwargs['path']

        files = {
            'quizzes.csv': self.import_quizzes,
            'categories.csv': self.import_categories,
            'questions.csv': self.import_questions,
        }

        for filename, func in files.items():
            file_path = os.path.join(directory_path, filename)

            if os.path.exists(file_path):
                try:
                    func(file_path)
                except Exception:
                    pass
            else:
                pass

    def import_categories(self, file_path: str) -> None:
        """
        Docstring для import_categories

        :param file_path: путь к файлу
        """
        df = pd.read_csv(file_path)
        categories = []
        for _, row in df.iterrows():
            categories.append(Category(
                id=row['id'],
                title=row['title'],
            ))
        Category.objects.bulk_create(categories)

    def import_quizzes(self, file_path: str) -> None:
        """
        Docstring для import_categories

        :param file_path: путь к файлу
        """
        df = pd.read_csv(file_path)
        quizzes = []
        for _, row in df.iterrows():
            quizzes.append(Quiz(
                id=row['id'],
                title=row['title'],
                description=row['description'],
            ))
        Quiz.objects.bulk_create(quizzes)

    def import_questions(self, file_path: str) -> None:
        """
        Docstring для import_categories

        :param file_path: путь к файлу
        """
        df = pd.read_csv(file_path)
        questions = []

        for _, row in df.iterrows():
            quiz = Quiz.objects.get(id=row['quiz_id'])
            category = Category.objects.get(id=row['category_id'])
            questions.append(Question(
                id=row['id'],
                category_id=category,
                quiz_id=quiz,
                text=row['text'],
                description=row['description'],
                options=ast.literal_eval(row['options'].replace('""', '"')),
                correct_answer=row['correct_answer'],
                explanation=row['explanation'],
                difficulty=row['difficulty']

            ))
        Question.objects.bulk_create(questions)
