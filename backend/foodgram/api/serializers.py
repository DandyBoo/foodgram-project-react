from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from recipes.models import Tag, Ingredient
from users.models import User, Follow


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей."""
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'is_subscribed'
        )

    def get_is_subscribed(self, obj: User):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return Follow.objects.filter(
            user=request.user, author=obj).exists()


class TagSerializer(ModelSerializer):
    """Сериализатор тегов."""
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class IngredientSerializer(ModelSerializer):
    """Сериализатор ингридиентов."""
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit'
        )


# ....

class SubsctiptionListSerializer(UserSerializer):
    """Сериализатор подписок."""
    pass
