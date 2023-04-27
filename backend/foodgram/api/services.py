import io
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics, ttfonts
from reportlab.pdfgen import canvas

from recipes.models import IngredientRecipe


def create_pdf(ingredients):
    creation_date = datetime.today().strftime('%Y-%m-%d')
    font = 'DejaVuSerif'
    pdfmetrics.registerFont(
        ttfonts.TTFont(font, './DejaVuSerif.ttf', 'utf-8')
    )
    buffer = io.BytesIO()
    page = canvas.Canvas(buffer, pagesize=A4)

    data = {
        ingredient['ingredient__name']: {
            ingredient['ingredient__measurement_unit']: ingredient['amount']
        } for ingredient in ingredients
    }
    page.setFont(font, 15, leading=None)
    page.setFillColorRGB(0.29296875, 0.453125, 0.609375)
    page.drawString(260, 800, 'Список ингредиентов')
    page.line(0, 780, 1000, 780)
    page.line(0, 778, 1000, 778)
    x1 = 20
    y1 = 750
    for key, value in data.items():
        page.setFont(font, 15, leading=None)
        page.drawString(x1, y1 - 12, f'{key}')
        for unit, amount in value.items():
            page.setFont(font, 10, leading=None)
            page.drawString(x1, y1 - 30, f'{unit} - {amount}')
            y1 = y1 - 60
    page.setTitle(f'Отправлено {creation_date}')
    page.showPage()
    page.save()
    buffer.seek(0)
    return buffer


def create_ingredients(recipe, ingredients):
    IngredientRecipe.objects.bulk_create([
        IngredientRecipe(
            recipe=recipe,
            amount=ingredient['amount'],
            ingredient=ingredient['ingredient'],
        ) for ingredient in ingredients
    ])
