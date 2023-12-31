from django.db import IntegrityError, transaction
from rest_framework import status, viewsets
from rest_framework.response import Response

from api.filtersets import AppointmentsFilterSet
from api.models import Appointment, HealthCareWorker
from api.serializers import AppointmentSerializer, HealthCareWorkerSerializer


class ListAsDictModelMixin:
    """
    List a queryset with dict-like response.

    Based on https://github.com/stickfigure/blog/wiki/How-to-(and-how-not-to)-design-REST-APIs#rule-4-dont-return-arrays-as-top-level-responses
    """
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        as_dict = {
            'data': serializer.data,
        }

        return Response(as_dict)


class HealthCareWorkersViewSet(ListAsDictModelMixin, viewsets.ModelViewSet):
    queryset = HealthCareWorker.objects.all()
    serializer_class = HealthCareWorkerSerializer
    lookup_field = 'uuid'
    lookup_value_converter = 'uuid'


class AppointmentsViewSet(ListAsDictModelMixin, viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    lookup_field = 'uuid'
    lookup_value_converter = 'uuid'
    filterset_class = AppointmentsFilterSet
