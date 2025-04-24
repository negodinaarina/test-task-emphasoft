from django.urls import path
from users.views import (
    UserListView,
    UserCreateView,
    TokenRefreshView,
    TokenObtainPairView,
    UserRetrieveView
)

app_name = "users"

urlpatterns = [
    path("users", UserListView.as_view()),
    path("create", UserCreateView.as_view()),
    path("login", TokenObtainPairView.as_view()),
    path("refresh", TokenRefreshView.as_view()),
    path("me", UserRetrieveView.as_view()),
]
