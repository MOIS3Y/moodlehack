from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("moodlehack.accounts.urls")),
    path("", include("moodlehack.answers.urls")),
]

urlpatterns += [
    # API Schema
    path("api/v1/schema/", SpectacularAPIView.as_view(), name="schema"),
    # API UI:
    path(
        "api/v1/schema/swagger/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui"
    ),
    # API Token Auth
    path("api/v1/auth", views.obtain_auth_token)
]
