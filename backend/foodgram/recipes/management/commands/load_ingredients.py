import csv

from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Loads the ingredients to database from csv file'

    def handle(self, *args, **options):
        with open('data/ingredients.csv', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            try:
                Ingredient.objects.bulk_create(
                    Ingredient(**items) for items in reader
                )
            except Exception as e:
                return f'Возникла ошибка при импорте из csv-файла: {e}'

        return (
            f'Загрузка прошла успешно,'
            f'всего загружено ингредиентов - {Ingredient.objects.count()}'
        )
