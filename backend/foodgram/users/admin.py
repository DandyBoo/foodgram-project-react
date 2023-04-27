from django.contrib import admin

from .models import Follow, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Административная панель пользователя."""
    list_display = (
        'id', 'username', 'email', 'first_name',
        'last_name', 'is_superuser'
    )
    list_filter = ('username', 'email')
    search_fields = ('username', 'email')


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """Административная панель подписок."""
    list_display = ('id', 'user', 'author')
