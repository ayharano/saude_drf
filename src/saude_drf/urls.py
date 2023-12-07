from django.urls import path, include


api_path = path(
    "api/",
    include('api.urls', namespace='api'),
)


urlpatterns = [
    api_path,
]
