from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


api_path = path(
    "api/",
    include('api.urls', namespace='api'),
)


urlpatterns = [
    path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    api_path,
]
