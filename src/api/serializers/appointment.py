from datetime import UTC, datetime

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from api.constants import (
    APPOINTMENT_DATE_ERROR_MESSAGE,
    UNIQUE_APPOINTMENT_DATE_HEALTH_CARE_WORKER_ERROR_MESSAGE,
)
from api.models import Appointment, HealthCareWorker


def build_field_name_mapping() -> tuple[dict[str, str], dict[str, str]]:
    model_serializer_fields_tuples = (
        ('uuid', 'uuid'),
        ('date', 'data'),
        ('info', 'info'),
    )

    model_to_serializer = {}
    serializer_to_model = {}

    for model_field, serializer_field in model_serializer_fields_tuples:
        model_to_serializer[model_field] = serializer_field
        serializer_to_model[serializer_field] = model_field

    return model_to_serializer, serializer_to_model


MODEL_TO_SERIALIZER, SERIALIZER_TO_MODEL = build_field_name_mapping()


del build_field_name_mapping


class StringSlugRelatedField(serializers.SlugRelatedField):
    def to_representation(self, obj):
        return str(getattr(obj, self.slug_field))


class AppointmentSerializer(serializers.ModelSerializer):
    profissional_uuid = StringSlugRelatedField(
        slug_field='uuid',
        queryset=HealthCareWorker.objects.all(),
        many=False,
        source='health_care_worker',
    )
    data = serializers.DateField(source='date')
    info = serializers.CharField()

    def validate_data(self, value):
        if value <= datetime.now(UTC).date():
            raise serializers.ValidationError(APPOINTMENT_DATE_ERROR_MESSAGE)
        return value

    class Meta:
        model = Appointment
        fields = [
            'uuid',
            'profissional_uuid',
            'data',
            'info',
            # 'id',  # we only use id internally - all external interactions use uuid
            # 'created',  # timestamp internal metadata
            # 'modified',  # timestamp internal metadata
        ]
        read_only_fields = [
            'uuid',
        ]
        validators = [
            UniqueTogetherValidator(
                queryset=Appointment.objects.all(),
                fields=['profissional_uuid', 'data'],
                message=UNIQUE_APPOINTMENT_DATE_HEALTH_CARE_WORKER_ERROR_MESSAGE,
            )
        ]
