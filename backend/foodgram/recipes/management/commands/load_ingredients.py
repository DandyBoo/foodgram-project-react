import csv

from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Loads the ingredients to database from csv file'

    def handle(self, *args, **options):
        with open('../../data/ingredients.csv', 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            try:
                Ingredient.objects.bulk_create(
                    Ingredient(name=item[0], measurement_unit=item[1]) for item in reader
                )
            except Exception as e:
                return f'Возникла ошибка при импорте из csv-файла: {e}'

        return (
            f'Загрузка прошла успешно,'
            f'всего загружено ингредиентов - {Ingredient.objects.count()}'
        )
