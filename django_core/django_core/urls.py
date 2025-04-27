from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

api_urlpatterns = [
    path("auth/", include("users.urls")),
    path("docs/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "docs/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path(
        "rooms/",
        include("rooms.urls"),
    ),
]

internal_urlpatterns = [
    path("admin/", admin.site.urls),
    path(settings.API_PREFIX, include(api_urlpatterns)),
]

urlpatterns = [
    path(settings.BASE_URL, include(internal_urlpatterns)),
]
