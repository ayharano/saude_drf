import uuid

from django.db import models
from django.db.models.functions import Now

from api.constants import (
    APPOINTMENT_DATE_CONSTRAINT_NAME,
    UNIQUE_APPOINTMENT_DATE_HEALTH_CARE_WORKER_CONSTRAINT_NAME,
)
from .base import BaseModel
from .health_care_worker import HealthCareWorker


class Appointment(BaseModel):
    health_care_worker = models.ForeignKey(HealthCareWorker, related_name='appointments', on_delete=models.CASCADE)
    date = models.DateField()
    info = models.TextField()

    class Meta:
        ordering = ['date']
        constraints = [
            models.UniqueConstraint(
                fields=["health_care_worker", "date"],
                name=UNIQUE_APPOINTMENT_DATE_HEALTH_CARE_WORKER_CONSTRAINT_NAME,
            ),
            models.CheckConstraint(
                check=models.Q(date__gt=Now()),
                name=APPOINTMENT_DATE_CONSTRAINT_NAME,
            ),
        ]
