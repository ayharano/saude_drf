from rest_framework import serializers

from api.models import HealthCareWorker


def build_field_name_mapping() -> tuple[dict[str, str], dict[str, str]]:
    model_serializer_fields_tuples = (
        ('uuid', 'uuid'),
        ('legal_name', 'nome_legal'),
        ('preferred_name', 'nome_social'),
        ('pronouns', 'pronomes'),
        ('date_of_birth', 'data_de_nascimento'),
        ('specialization', 'especializacao'),
    )

    model_to_serializer = {}
    serializer_to_model = {}

    for model_field, serializer_field in model_serializer_fields_tuples:
        model_to_serializer[model_field] = serializer_field
        serializer_to_model[serializer_field] = model_field

    return model_to_serializer, serializer_to_model


MODEL_TO_SERIALIZER, SERIALIZER_TO_MODEL = build_field_name_mapping()


del build_field_name_mapping


class HealthCareWorkerSerializer(serializers.ModelSerializer):
    nome_legal = serializers.CharField(source='legal_name')
    nome_social = serializers.CharField(source='preferred_name', allow_blank=True)
    pronomes = serializers.CharField(source='pronouns')

    data_de_nascimento = serializers.DateField(source='date_of_birth')

    especializacao = serializers.CharField(source='specialization')

    class Meta:
        model = HealthCareWorker
        fields = [
            'uuid',
            'nome_legal',
            'nome_social',
            'pronomes',
            'data_de_nascimento',
            'especializacao',
            # 'id',  # we only use id internally - all external interactions use uuid
            # 'created',  # timestamp internal metadata
            # 'modified',  # timestamp internal metadata
        ]
        read_only_fields = [
            'uuid',
        ]
