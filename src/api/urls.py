from rest_framework import routers


app_name = 'api'


router = routers.DefaultRouter(
    trailing_slash=False,
)


urlpatterns = router.urls
