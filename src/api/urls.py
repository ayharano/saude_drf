from rest_framework import routers

from api.views import AppointmentsViewSet, HealthCareWorkersViewSet


app_name = 'api'


router = routers.DefaultRouter(
    trailing_slash=False,
)
router.register(
    'consultas', AppointmentsViewSet, basename='appointments',
)
router.register(
    'profissionais', HealthCareWorkersViewSet, basename='health-care-workers',
)


urlpatterns = router.urls
