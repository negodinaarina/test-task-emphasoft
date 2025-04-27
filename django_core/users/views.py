from django.utils.decorators import method_decorator
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.models import User
from users.serializers import UserCreateSerializer, UserRetrieveSerializer


@method_decorator(
    name="post",
    decorator=extend_schema(
        request=UserCreateSerializer, responses=UserRetrieveSerializer
    ),
)
class UserCreateView(generics.CreateAPIView):
    """
    Create new user
    """

    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]


@method_decorator(
    name="get",
    decorator=extend_schema(responses=UserRetrieveSerializer),
)
class UserListView(generics.ListAPIView):
    """
    Get all users
    """

    queryset = User.objects.all()
    serializer_class = UserRetrieveSerializer
    permission_classes = [IsAdminUser]


class UserRetrieveView(generics.RetrieveAPIView):
    """
    Get information about current user
    """

    permission_classes = [IsAuthenticated]
    serializer_class = UserRetrieveSerializer

    def get_object(self):
        return self.request.user
