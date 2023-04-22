from django.db.models import Subquery, Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from recipes.models import (Cart, Favorite, Ingredient, IngredientRecipe,
                            Recipe, Tag)
from users.models import Follow, User

from . import serializers
from .filters import IngredientFilter, RecipeFilter
from .mixins import CreateAndDeleteRelatedMixin
from .pagination import CustomPagination
from .permissions import IsAuthorOrAdminOrReadOnly
from .services import create_pdf


class UserViewSet(DjoserUserViewSet):
    pagination_class = CustomPagination

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)

        if request.method == 'POST':
            serializer = serializers.FollowSerializer(
                author, data=request.data, context={"request": request}
            )
            serializer.is_valid(raise_exception=True)
            Follow.objects.create(user=user, author=author)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        elif request.method == "DELETE":
            get_object_or_404(
                Follow, user=user, author=author
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError('Неверный метод запроса.')

    @action(
        methods=['get'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(following__user=user)
        pages = self.paginate_queryset(queryset)
        serializer = serializers.FollowListSerializer(
            pages, many=True, context={"request": request}
        )
        return self.get_paginated_response(serializer.data)


class TagViewSet(ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer


class IngredientViewSet(ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    filter_backends = (IngredientFilter,)
    search_fields = ('^name',)


class RecipeViewSet(ModelViewSet, CreateAndDeleteRelatedMixin):
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = (IsAuthorOrAdminOrReadOnly,)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return serializers.RecipeSerializer
        return serializers.CreateRecipeSerializer

    @action(methods=['post'], detail=True)
    def shopping_cart(self, request, pk):
        return self._create_related(
            request, pk, serializers=serializers.CartSerializer
        )

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return self._delete_related(
            request=request, pk=pk, model=Cart)

    @action(detail=False, methods=["GET"])
    def download_shopping_cart(self, request):
        recipes_in_cart = Cart.objects.filter(user=request.user)
        ingredients = IngredientRecipe.objects.filter(
            recipe__in=Subquery(recipes_in_cart.values("pk"))
        ).order_by("ingredient__name").values(
            "ingredient__name", "ingredient__measurement_unit"
        ).annotate(amount=Sum("amount"))
        return FileResponse(
            create_pdf(ingredients),
            as_attachment=True,
            filename='shopping_cart.pdf')

    @action(methods=['post'], detail=True)
    def favorite(self, request, pk):
        return self._create_related(
            request=request, pk=pk, serializers=serializers.FollowSerializer)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        return self._delete_related(
            request=request, pk=pk, model=Favorite)
