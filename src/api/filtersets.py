from django_filters import rest_framework as filters

from api.models import Appointment


class AppointmentsFilterSet(filters.FilterSet):
    profissional_uuid = filters.UUIDFilter(field_name='health_care_worker__uuid')

    class Meta:
        model = Appointment
        fields = []
