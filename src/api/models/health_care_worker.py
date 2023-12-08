import uuid

from django.db import models

from .base import BaseModel


class HealthCareWorker(BaseModel):
    legal_name = models.CharField(max_length=255)
    preferred_name = models.CharField(max_length=255, blank=True)
    pronouns = models.CharField(max_length=255)

    date_of_birth = models.DateField()

    specialization = models.CharField(max_length=255)
