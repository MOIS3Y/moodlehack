from django.contrib import admin
from django.urls import path, include

from rest_framework.authtoken import views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('answers.urls')),
    path("accounts/", include("accounts.urls")),
]


urlpatterns += [
    # API PATTERNS
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    # Optional UI:
    path(
        'api/v1/schema/swagger/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui'
    ),
    # API Token auth
    path('api/v1/auth', views.obtain_auth_token)
]
