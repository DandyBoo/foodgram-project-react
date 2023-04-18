from djoser.views import UserViewSet

from .pagination import CustomPagination
from .serializers import UserSerializer
from users.models import User


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = CustomPagination

