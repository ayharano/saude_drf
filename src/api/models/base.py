import uuid

from django.db import models
from model_utils.models import TimeStampedModel


# Based on https://buildkite.com/blog/goodbye-integers-hello-uuids
# as UUIDv7 is not available yet
# ( source: https://github.com/python/cpython/issues/89083 )
class IdUuidModel(models.Model):
    id = models.AutoField(primary_key=True)
    uuid = models.UUIDField(
        unique=True,
        default=uuid.uuid4,
        editable=False,
    )

    class Meta:
        abstract = True


class BaseModel(IdUuidModel, TimeStampedModel, models.Model):
    class Meta:
        abstract = True
