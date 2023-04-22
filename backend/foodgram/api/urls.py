from django.urls import include, path
from rest_framework import routers

from .views import IngredientViewSet, RecipeViewSet, TagViewSet, UserViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
