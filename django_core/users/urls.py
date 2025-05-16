from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import CurrentUserViewSet, TokenObtainPairView, TokenRefreshView, UserViewSet

app_name = "users"


router = DefaultRouter()
router.register(r'', UserViewSet, basename='users')
router.register(r'me', CurrentUserViewSet, basename='current-user')


urlpatterns = [
    path("login", TokenObtainPairView.as_view()),
    path("refresh", TokenRefreshView.as_view()),
    path("", include(router.urls)),
]
