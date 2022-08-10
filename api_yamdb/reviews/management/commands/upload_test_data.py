import csv
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from api_yamdb.settings import BASE_DIR

User = get_user_model()


class Command(BaseCommand):
    help = 'Заливает тестовые данные из csv файлов в папке static/data'

    def handle(self, *args, **options):
        try:
            from reviews.models import Category, Genre, Title
            self.stdout.write('Модели Category/Genre/Title импортированы')

            files_models = (
                ('static/data/category.csv', Category),
                ('static/data/genre.csv', Genre),
                # ('static/data/titles.csv', Title),       ValueError: Cannot assign "'1'": "Title.category" must be a "Category" instance.
                ('static/data/users.csv', User),
            )
            for file, class_name in files_models:
                file_name = os.path.join(BASE_DIR, file)
                with open(file_name, newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    counter = 0
                    for row in reader:
                        class_name.objects.update_or_create(
                            id=row['id'], defaults=row)
                        counter += 1
                msg = f'Залито объектов {class_name.__name__}: {counter}'
                self.stdout.write(msg)
        except ImportError:
            self.stdout.write('Не могу импортировать Category/Genre/Title')

        try:
            from reviews.models import Comment, Review
            self.stdout.write('Модели Review / Comment импортированы')
            files_models = (
                # ('static/data/review.csv', Review),
                # ('static/data/comments.csv', Comment),
            )
            for file, class_name in files_models:
                file_name = os.path.join(BASE_DIR, file)
                with open(file_name, newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        class_name.objects.update_or_create(
                            id=row['id'], defaults=row)
                obj_count = class_name.objects.count()
                self.stdout.write(f'Залито {obj_count} объектов {class_name}')
        except ImportError:
            self.stdout.write('Не могу импортировать Review / Comment')
