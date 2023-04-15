from django.contrib import admin
from django.contrib.admin import TabularInline

from .models import Cart, Favorite, Ingredient, IngredientRecipe, Recipe, Tag


class IngredientInline(TabularInline):
    """Вспомогательный класс для отображения ингредиентов в модели рецептов."""
    model = IngredientRecipe


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Административная панель тегов."""
    list_display = ('name', 'color', 'slug')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Административная панель ингридиентов."""
    list_display = ('pk', 'name', 'measurement_unit')
    list_editable = ('name', 'measurement_unit',)
    list_filter = ('measurement_unit',)
    search_fields = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Административная панель рецептов."""
    list_display = ('name', 'author')
    inlines = (IngredientInline,)


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Административная панель избранных рецептов."""
    list_display = ('user', 'recipe')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Административная панель корзины."""
    list_display = ('recipe', 'user')
