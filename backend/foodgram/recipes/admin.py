from django.contrib import admin

from .models import Tag, Ingredient, Recipe, Favorite, Cart


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Административная панель тегов."""
    list_display = ('name', 'color', 'slug')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Административная панель ингридиентов."""
    list_display = ('name', 'measurement_unit')
    list_filter = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Административная панель рецептов."""
    list_display = ('name', 'author')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Административная панель избранных рецептов."""
    list_display = ('user', 'recipe')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Административная панель корзины."""
    list_display = ('recipe', 'user')
