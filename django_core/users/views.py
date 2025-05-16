from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from users.models import User
from users.serializers import UserCreateSerializer, UserRetrieveSerializer


@extend_schema_view(
    create=extend_schema(
        request=UserCreateSerializer,
        responses=UserRetrieveSerializer,
    ),
    list=extend_schema(
        responses=UserRetrieveSerializer,
    ),
)
class UserViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """
    - User creation (open to all)
    - Listing all users (admin only)
    """

    queryset = User.objects.all()

    def get_permissions(self):
        if self.action == "create":
            return [AllowAny()]
        elif self.action == "list":
            return [IsAdminUser()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return UserRetrieveSerializer


class CurrentUserViewSet(viewsets.ViewSet):
    """
    Get information about current user
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses=UserRetrieveSerializer,
    )
    def list(self, request):
        serializer = UserRetrieveSerializer(request.user)
        return Response(serializer.data)
