from django.contrib import admin

from .models import Cart, Favorite, Ingredient, IngredientRecipe, Recipe, Tag


class IngredientInline(admin.TabularInline):
    """Вспомогательный класс для отображения ингредиентов в модели рецептов."""
    model = IngredientRecipe
    min_num = 1


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Административная панель тегов."""
    list_display = ('name', 'color', 'slug')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    """Административная панель ингридиентов."""
    list_display = ('pk', 'name', 'measurement_unit')
    list_editable = ('name', 'measurement_unit',)
    list_filter = ('name',)
    search_fields = ('name',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    """Административная панель рецептов."""
    list_display = ('name', 'author', 'display_favorite', 'pub_date')
    list_filter = ('author', 'name', 'tags')
    search_fields = ('name',)
    inlines = (IngredientInline,)

    def display_favorite(self, obj):
        return Favorite.objects.filter(recipe=obj).count()

    display_favorite.short_description = 'Добавлено в избранное'


@admin.register(IngredientRecipe)
class IngredientRecipeAdmin(admin.ModelAdmin):
    """Административная панель ингридиентов в рецепте."""
    list_display = (
        'recipe',
        'ingredient',
        'amount',
    )
    list_filter = ('recipe', 'ingredient')


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Административная панель избранных рецептов."""
    list_display = ('user', 'recipe')


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Административная панель корзины."""
    list_display = ('recipe', 'user')
