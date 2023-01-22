import csv
import os

from django.core.management import BaseCommand
from api_yamdb.settings import CSV_FILES_DIR

from reviews.models import (
    Category,
    GenreTitle,
    Review,
    Title,
    Comment,
    Genre,
)

from users.models import User

FILES_CLASSES = {
    'category': Category,
    'genre': Genre,
    'titles': Title,
    'genre_title': GenreTitle,
    'users': User,
    'review': Review,
    'comments': Comment,
}

FIELDS = {
    'category': ('category', Category),
    'title_id': ('title', Title),
    'genre_id': ('genre', Genre),
    'author': ('author', User),
    'review_id': ('review', Review),
}


def open_csv(file_name):
    csv_file = file_name + '.csv'
    csv_path = os.path.join(CSV_FILES_DIR, csv_file)
    with (open(csv_path, encoding='utf-8')) as file:
        return list(csv.reader(file))


def change_values(data_csv):
    data_csv_copy = data_csv.copy()
    for field_key, field_value in data_csv.items():
        if field_key in FIELDS.keys():
            field_keyNULL = FIELDS[field_key][0]
            data_csv_copy[field_keyNULL] = FIELDS[field_key][1].objects.get(
                pk=field_value)
    return data_csv_copy


def load_csv(file_name, class_name):
    data = open_csv(file_name)
    rows = data[1:]
    for row in rows:
        data_csv = dict(zip(data[0], row))
        data_csv = change_values(data_csv)
        table = class_name(**data_csv)
        table.save()


class Command(BaseCommand):

    def handle(self, *args, **options):
        for key, value in FILES_CLASSES.items():
            print(f'Загрузка таблицы {value.__qualname__}')
            load_csv(key, value)
