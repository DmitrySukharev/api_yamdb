import csv
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import connection

from api_yamdb.settings import BASE_DIR

DATA_DIR = os.path.join(BASE_DIR, 'static/data/')
User = get_user_model()


class Command(BaseCommand):
    help = 'Заливает тестовые данные из csv файлов в папке static/data'

    def handle(self, *args, **options):
        try:
            from reviews.models import Category, Genre, Title
            self.stdout.write('Модели Category/Genre/Title импортированы')

            files_models = (
                ('category.csv', Category),
                ('genre.csv', Genre),
                ('titles.csv', Title),
                ('users.csv', User),
            )
            for file, class_name in files_models:
                file_path = os.path.join(DATA_DIR, file)
                with open(file_path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    counter = 0
                    for row in reader:
                        if class_name == Title:
                            cat_id = row['category']
                            row['category'] = Category.objects.get(id=cat_id)
                        class_name.objects.update_or_create(
                            id=row['id'], defaults=row)
                        counter += 1
                msg = f'Залито объектов {class_name.__name__}: {counter}'
                self.stdout.write(msg)
        except ImportError:
            self.stdout.write('Не могу импортировать Category/Genre/Title')
        except FileNotFoundError:
            raise CommandError('Как минимум один из csv файлов отсутствует!')

        try:
            from reviews.models import Comment, Review
            self.stdout.write('Модели Review / Comment импортированы')
            files_models = (
                # ('static/data/review.csv', Review),       # Требуется прописать в row объекты вместо id для связанных полей, как для Title Category
                # ('static/data/comments.csv', Comment),    # Требуется прописать в row объекты вместо id для связанных полей, как для Title Category
            )
            for file, class_name in files_models:
                file_path = os.path.join(DATA_DIR, file)
                with open(file_path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    counter = 0
                    for row in reader:
                        class_name.objects.update_or_create(
                            id=row['id'], defaults=row)
                        counter += 1
                msg = f'Залито объектов {class_name.__name__}: {counter}'
                self.stdout.write(msg)
        except ImportError:
            self.stdout.write('Не могу импортировать Review / Comment')
        except FileNotFoundError:
            raise CommandError('Как минимум один из csv файлов отсутствует!')

        # Заливка из genre_title.csv напрямую в SQL таблицу title_genres
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM title_genres")
            row_count = cursor.fetchone()[0]
            if row_count == 0:
                file_path = os.path.join(DATA_DIR, 'genre_title.csv')
                with open(file_path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        sql_stmt = "INSERT INTO title_genres VALUES (%s,%s,%s)"
                        params = (row['id'], row['title_id'], row['genre_id'])
                        cursor.execute(sql_stmt, [*params])
                    cursor.execute("SELECT COUNT(*) FROM title_genres")
                    row_count = cursor.fetchone()[0]
                    msg = f'Залито записей в title_genre: {row_count}'
                    self.stdout.write(msg)
            else:
                msg = 'Таблица title_genres не пуста, заливка csv отменена'
                self.stdout.write(msg)
